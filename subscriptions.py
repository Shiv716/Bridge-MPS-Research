from __future__ import annotations
"""
Bridge – Subscriptions Module
DB-backed. Stores in subscriptions table.
"""

import secrets
from datetime import datetime
from db import db_subscribe, db_unsubscribe, db_get_subscriptions, db_is_subscribed, db_notify_subscribers


def _serialize_sub(sub: dict) -> dict:
    """Convert datetime fields for JSON."""
    out = {}
    for k, v in sub.items():
        if isinstance(v, datetime):
            out[k] = v.timestamp()
        else:
            out[k] = v
    return out


async def subscribe(user_id: str, provider_id: str, provider_name: str, user_email: str = "") -> dict:
    sub_id = f"sub-{secrets.token_hex(6)}"
    sub = await db_subscribe(
        sub_id=sub_id, user_id=user_id, user_email=user_email,
        provider_id=provider_id, provider_name=provider_name,
    )
    return _serialize_sub(sub)


async def unsubscribe(user_id: str, provider_id: str) -> bool:
    return await db_unsubscribe(user_id, provider_id)


async def get_subscriptions(user_id: str) -> list[dict]:
    subs = await db_get_subscriptions(user_id)
    return [_serialize_sub(s) for s in subs]


async def is_subscribed(user_id: str, provider_id: str) -> bool:
    return await db_is_subscribed(user_id, provider_id)


async def notify_subscribers(provider_id: str) -> list[dict]:
    subs = await db_notify_subscribers(provider_id)
    return [_serialize_sub(s) for s in subs]
