from __future__ import annotations
"""
Bridge – Messaging Module
Adviser-to-Bridge messaging. In-memory store for demo; replace with DB later.
"""

import time
import secrets
from typing import Optional

# ─── Message Store (replace with DB later) ────────────────────────────

MESSAGES: list[dict] = []


def send_message(
    user_id: str,
    user_name: str,
    user_firm: str,
    subject: str,
    body: str,
    provider_id: Optional[str] = None,
    provider_name: Optional[str] = None,
) -> dict:
    """Send a message from adviser to Bridge."""
    msg = {
        "id": f"msg-{secrets.token_hex(6)}",
        "user_id": user_id,
        "user_name": user_name,
        "user_firm": user_firm,
        "subject": subject,
        "body": body,
        "provider_id": provider_id,
        "provider_name": provider_name,
        "status": "sent",
        "reply": None,
        "created_at": time.time(),
        "replied_at": None,
    }
    MESSAGES.append(msg)
    return msg


def get_messages(user_id: str) -> list[dict]:
    """Get all messages for a user, newest first."""
    return sorted(
        [m for m in MESSAGES if m["user_id"] == user_id],
        key=lambda m: m["created_at"],
        reverse=True,
    )


def get_message_by_id(message_id: str, user_id: str) -> Optional[dict]:
    """Get a specific message (only if it belongs to the user)."""
    return next(
        (m for m in MESSAGES if m["id"] == message_id and m["user_id"] == user_id),
        None,
    )
