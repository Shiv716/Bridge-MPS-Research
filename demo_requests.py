from __future__ import annotations
"""
Bridge – Demo Requests Module
Handles demo request submissions, admin approval, and auto-account creation.
"""

import secrets
from datetime import datetime, timezone
from typing import Optional

from db import database
from auth import create_invite


# ─── DB Queries ───────────────────────────────────────────────────────

async def create_demo_request(*, name: str, email: str, firm: str, persona: str = "", tier: str = "") -> dict:
    req_id = f"demo-{secrets.token_hex(6)}"
    await database.execute(
        """INSERT INTO demo_requests (id, name, email, firm, persona, tier)
        VALUES (:id, :name, :email, :firm, :persona, :tier)""",
        {"id": req_id, "name": name, "email": email.lower().strip(), "firm": firm, "persona": persona, "tier": tier},
    )
    return await get_demo_request(req_id)


async def get_demo_request(req_id: str) -> dict | None:
    row = await database.fetch_one("SELECT * FROM demo_requests WHERE id = :id", {"id": req_id})
    return _serialize(dict(row._mapping)) if row else None


async def get_all_demo_requests(status: str = None) -> list[dict]:
    if status:
        rows = await database.fetch_all(
            "SELECT * FROM demo_requests WHERE status = :status ORDER BY created_at DESC",
            {"status": status},
        )
    else:
        rows = await database.fetch_all("SELECT * FROM demo_requests ORDER BY created_at DESC")
    return [_serialize(dict(r._mapping)) for r in rows]


async def approve_demo_request(req_id: str, approved_by: str) -> dict | None:
    """Approve a demo request: create user account + invite token."""
    req = await get_demo_request(req_id)
    if not req or req["status"] != "pending":
        return None

    # Create invite (this creates the user + invite token)
    result = await create_invite(
        email=req["email"],
        name=req["name"],
        firm=req["firm"],
        role="adviser",
        invited_by=approved_by,
    )

    # Update request status
    await database.execute(
        "UPDATE demo_requests SET status = 'approved', reviewed_by = :by, reviewed_at = NOW() WHERE id = :id",
        {"by": approved_by, "id": req_id},
    )

    return {"request": await get_demo_request(req_id), "invite": result}


async def reject_demo_request(req_id: str, rejected_by: str) -> dict | None:
    """Reject a demo request."""
    req = await get_demo_request(req_id)
    if not req or req["status"] != "pending":
        return None

    await database.execute(
        "UPDATE demo_requests SET status = 'rejected', reviewed_by = :by, reviewed_at = NOW() WHERE id = :id",
        {"by": rejected_by, "id": req_id},
    )

    return await get_demo_request(req_id)


async def get_pending_count() -> int:
    row = await database.fetch_one("SELECT COUNT(*) as count FROM demo_requests WHERE status = 'pending'")
    return row["count"] if row else 0


# ─── Helpers ──────────────────────────────────────────────────────────

def _serialize(d: dict) -> dict:
    out = {}
    for k, v in d.items():
        if isinstance(v, datetime):
            out[k] = v.isoformat()
        else:
            out[k] = v
    return out
