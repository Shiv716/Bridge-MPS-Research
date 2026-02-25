from __future__ import annotations
"""
Bridge – User Preferences Module
Display settings, notification frequency, and per-subscription alert toggles.
In-memory store for demo; replace with DB later.
"""

from typing import Optional

# ─── Defaults ─────────────────────────────────────────────────────────

DEFAULT_PREFERENCES = {
    "display": {
        "default_risk_level": 7,
        "dark_mode": False,
    },
    "notifications": {
        "frequency": "instant",  # instant | daily | weekly
    },
    "subscription_alerts": {},  # provider_id -> True/False
}

# ─── Preferences Store (replace with DB later) ───────────────────────

USER_PREFERENCES: dict[str, dict] = {}


def get_preferences(user_id: str) -> dict:
    """Get user preferences, returning defaults for any missing keys."""
    prefs = USER_PREFERENCES.get(user_id, {})
    return {
        "display": {
            **DEFAULT_PREFERENCES["display"],
            **prefs.get("display", {}),
        },
        "notifications": {
            **DEFAULT_PREFERENCES["notifications"],
            **prefs.get("notifications", {}),
        },
        "subscription_alerts": {
            **DEFAULT_PREFERENCES.get("subscription_alerts", {}),
            **prefs.get("subscription_alerts", {}),
        },
    }


def update_preferences(user_id: str, updates: dict) -> dict:
    """Merge partial updates into user preferences."""
    current = get_preferences(user_id)

    if "display" in updates:
        current["display"].update(updates["display"])
    if "notifications" in updates:
        current["notifications"].update(updates["notifications"])
    if "subscription_alerts" in updates:
        current["subscription_alerts"].update(updates["subscription_alerts"])

    USER_PREFERENCES[user_id] = current
    return current


def set_subscription_alert(user_id: str, provider_id: str, enabled: bool) -> dict:
    """Toggle email alerts for a specific subscription."""
    prefs = get_preferences(user_id)
    prefs["subscription_alerts"][provider_id] = enabled
    USER_PREFERENCES[user_id] = prefs
    return prefs


def should_alert(user_id: str, provider_id: str) -> bool:
    """Check if alerts are enabled for a subscription (default True)."""
    prefs = get_preferences(user_id)
    return prefs["subscription_alerts"].get(provider_id, True)
