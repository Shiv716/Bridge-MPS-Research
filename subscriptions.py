from __future__ import annotations
"""
Bridge – Subscriptions Module
Subscribe to MPS ranges for email alerts on data updates.
In-memory store for demo; replace with DB later.
"""

import time
from typing import Optional

# ─── Subscription Store (replace with DB later) ──────────────────────

SUBSCRIPTIONS: list[dict] = []


def subscribe(user_id: str, provider_id: str, provider_name: str, user_email: str = "") -> dict:
    """Subscribe user to an MPS range."""
    # Check if already subscribed
    existing = next(
        (s for s in SUBSCRIPTIONS
         if s["user_id"] == user_id and s["provider_id"] == provider_id and s["active"]),
        None,
    )
    if existing:
        return existing

    sub = {
        "id": f"sub-{len(SUBSCRIPTIONS)+1:04d}",
        "user_id": user_id,
        "user_email": user_email,
        "provider_id": provider_id,
        "provider_name": provider_name,
        "active": True,
        "created_at": time.time(),
    }
    SUBSCRIPTIONS.append(sub)
    return sub


def unsubscribe(user_id: str, provider_id: str) -> bool:
    """Unsubscribe user from an MPS range."""
    for sub in SUBSCRIPTIONS:
        if sub["user_id"] == user_id and sub["provider_id"] == provider_id and sub["active"]:
            sub["active"] = False
            return True
    return False


def get_subscriptions(user_id: str) -> list[dict]:
    """Get all active subscriptions for a user."""
    return [s for s in SUBSCRIPTIONS if s["user_id"] == user_id and s["active"]]


def is_subscribed(user_id: str, provider_id: str) -> bool:
    """Check if user is subscribed to a provider."""
    return any(
        s["user_id"] == user_id and s["provider_id"] == provider_id and s["active"]
        for s in SUBSCRIPTIONS
    )


def notify_subscribers(provider_id: str) -> list[dict]:
    """
    Get all subscribers for a provider (for sending email alerts).
    In production, this would trigger actual emails via Resend/SendGrid.
    """
    return [s for s in SUBSCRIPTIONS if s["provider_id"] == provider_id and s["active"]]
