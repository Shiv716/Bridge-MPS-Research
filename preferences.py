from __future__ import annotations
"""
Bridge – User Preferences Module
DB-backed. Stores as JSONB in user_preferences table.
"""

from db import db_get_preferences, db_upsert_preferences

DEFAULT_PREFERENCES = {
    "display": {
        "default_risk_level": 7,
        "dark_mode": False,
    },
    "notifications": {
        "frequency": "instant",
    },
    "subscription_alerts": {},
}


async def get_preferences(user_id: str) -> dict:
    stored = await db_get_preferences(user_id)
    prefs = stored or {}
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


async def update_preferences(user_id: str, updates: dict) -> dict:
    current = await get_preferences(user_id)
    if "display" in updates:
        current["display"].update(updates["display"])
    if "notifications" in updates:
        current["notifications"].update(updates["notifications"])
    if "subscription_alerts" in updates:
        current["subscription_alerts"].update(updates["subscription_alerts"])
    await db_upsert_preferences(user_id, current)
    return current


async def set_subscription_alert(user_id: str, provider_id: str, enabled: bool) -> dict:
    prefs = await get_preferences(user_id)
    prefs["subscription_alerts"][provider_id] = enabled
    await db_upsert_preferences(user_id, prefs)
    return prefs


async def should_alert(user_id: str, provider_id: str) -> bool:
    prefs = await get_preferences(user_id)
    return prefs["subscription_alerts"].get(provider_id, True)
