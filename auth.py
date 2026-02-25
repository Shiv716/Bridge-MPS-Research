from __future__ import annotations
"""
Bridge – Authentication Module
Demo auth with hardcoded credentials. Structured for real auth integration later.
Replace USERS dict and verify_password with DB lookups when ready.
"""

import hashlib
import secrets
import time
from typing import Optional

# ─── Demo Users (replace with DB later) ──────────────────────────────

USERS = {
    "demo@bridge.co.uk": {
        "id": "user-001",
        "email": "demo@bridge.co.uk",
        "password_hash": hashlib.sha256("Bridge2026!".encode()).hexdigest(),
        "name": "Demo Adviser",
        "firm": "Bridge Demo Firm",
        "role": "adviser",
    },
}

# ─── Session Store (replace with Redis/DB later) ─────────────────────

SESSIONS: dict[str, dict] = {}
SESSION_TTL = 86400  # 24 hours


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(email: str, password: str) -> Optional[dict]:
    """Verify credentials. Returns user dict or None."""
    user = USERS.get(email.lower().strip())
    if not user:
        return None
    if user["password_hash"] != _hash_password(password):
        return None
    return {k: v for k, v in user.items() if k != "password_hash"}


def create_session(user: dict) -> str:
    """Create a session token for an authenticated user."""
    token = secrets.token_urlsafe(32)
    SESSIONS[token] = {
        "user": user,
        "created": time.time(),
        "last_active": time.time(),
    }
    return token


def get_session(token: str) -> Optional[dict]:
    """Retrieve session by token. Returns user dict or None."""
    session = SESSIONS.get(token)
    if not session:
        return None
    if time.time() - session["created"] > SESSION_TTL:
        SESSIONS.pop(token, None)
        return None
    session["last_active"] = time.time()
    return session["user"]


def destroy_session(token: str):
    """Log out — remove session."""
    SESSIONS.pop(token, None)


def get_user_by_id(user_id: str) -> Optional[dict]:
    """Look up user by ID."""
    for user in USERS.values():
        if user["id"] == user_id:
            return {k: v for k, v in user.items() if k != "password_hash"}
    return None
