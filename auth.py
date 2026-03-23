from __future__ import annotations
"""
Bridge – Authentication Module
Bcrypt password hashing, DB-backed sessions, invite & reset token flows.
"""

import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt

from db import (
    get_user_by_email, get_user_by_id, create_user, set_user_password,
    create_session_row, get_session_row, delete_session_row,
    create_invite_token, get_invite_token, mark_invite_used,
    create_reset_token, get_reset_token, mark_reset_used,
    list_all_users, delete_user,
)

SESSION_TTL_HOURS = 24
INVITE_TTL_HOURS = 72
RESET_TTL_HOURS = 1


# ─── Password Hashing ────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except Exception:
        return False


# ─── Authentication ───────────────────────────────────────────────────

async def authenticate(email: str, password: str) -> Optional[dict]:
    """Verify credentials. Returns user dict (without hash) or None."""
    user = await get_user_by_email(email)
    if not user:
        return None
    if not user.get("password_hash"):
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return _safe_user(user)


# ─── Sessions ─────────────────────────────────────────────────────────

async def create_session(user: dict) -> str:
    """Create a DB-backed session token."""
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(hours=SESSION_TTL_HOURS)
    await create_session_row(token, user["id"], expires)
    return token


async def get_session(token: str) -> Optional[dict]:
    """Retrieve session. Returns user dict or None."""
    row = await get_session_row(token)
    if not row:
        return None
    return {
        "id": row["user_id"],
        "email": row["email"],
        "name": row["name"],
        "firm": row["firm"],
        "role": row["role"],
    }


async def destroy_session(token: str):
    await delete_session_row(token)


# ─── Invite Flow ──────────────────────────────────────────────────────

async def create_invite(*, email: str, name: str, firm: str, role: str = "adviser", invited_by: str) -> dict:
    """
    Admin creates an invite. Creates a user record (no password) and an invite token.
    Returns the invite token and user info.
    """
    # Check if user already exists
    existing = await get_user_by_email(email)
    if existing:
        raise ValueError(f"User with email {email} already exists")

    user_id = f"user-{secrets.token_hex(6)}"
    user = await create_user(user_id=user_id, email=email, name=name, firm=firm, role=role)

    token = secrets.token_urlsafe(48)
    expires = datetime.now(timezone.utc) + timedelta(hours=INVITE_TTL_HOURS)
    await create_invite_token(token, email, invited_by, expires)

    return {"token": token, "user": _safe_user(user)}


async def accept_invite(token: str, password: str) -> Optional[dict]:
    """
    User accepts invite by setting their password.
    Returns user dict or None if token invalid.
    """
    invite = await get_invite_token(token)
    if not invite:
        return None

    user = await get_user_by_email(invite["email"])
    if not user:
        return None

    pw_hash = hash_password(password)
    await set_user_password(user["id"], pw_hash)
    await mark_invite_used(token)

    return _safe_user(await get_user_by_id(user["id"]))


# ─── Password Reset Flow ─────────────────────────────────────────────

async def request_password_reset(email: str) -> Optional[str]:
    """
    Generate a reset token for the user. Returns the token or None if user not found.
    """
    user = await get_user_by_email(email)
    if not user:
        return None

    token = secrets.token_urlsafe(48)
    expires = datetime.now(timezone.utc) + timedelta(hours=RESET_TTL_HOURS)
    await create_reset_token(token, user["id"], expires)

    return token


async def complete_password_reset(token: str, new_password: str) -> Optional[dict]:
    """
    Reset password using token. Returns user dict or None if token invalid.
    """
    reset = await get_reset_token(token)
    if not reset:
        return None

    pw_hash = hash_password(new_password)
    await set_user_password(reset["user_id"], pw_hash)
    await mark_reset_used(token)

    return _safe_user(await get_user_by_id(reset["user_id"]))


# ─── Admin ────────────────────────────────────────────────────────────

async def get_all_users() -> list[dict]:
    users = await list_all_users()
    return [_safe_user(u) for u in users]


async def remove_user(user_id: str):
    await delete_user(user_id)


# ─── Helpers ──────────────────────────────────────────────────────────

def _safe_user(user: dict) -> dict:
    """Strip sensitive fields."""
    return {k: v for k, v in user.items() if k not in ("password_hash",)}
