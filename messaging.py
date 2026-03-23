from __future__ import annotations
"""
Bridge – Messaging Module
DB-backed. Stores in messages + message_replies tables.
"""

import secrets
from datetime import datetime
from typing import Optional
from db import db_send_message, db_get_messages, db_get_message_by_id, db_get_message_by_id_internal, db_reply_to_message


def _serialize_msg(msg: dict) -> dict:
    """Convert datetime fields for JSON."""
    out = {}
    for k, v in msg.items():
        if isinstance(v, datetime):
            out[k] = v.timestamp()
        elif k == "replies" and isinstance(v, list):
            out[k] = [{kk: vv.timestamp() if isinstance(vv, datetime) else vv for kk, vv in rep.items()} for rep in v]
        else:
            out[k] = v
    return out


async def send_message(
    user_id: str,
    user_name: str,
    user_firm: str,
    subject: str,
    body: str,
    provider_id: Optional[str] = None,
    provider_name: Optional[str] = None,
) -> dict:
    msg_id = f"msg-{secrets.token_hex(6)}"
    msg = await db_send_message(
        msg_id=msg_id, user_id=user_id, user_name=user_name, user_firm=user_firm,
        subject=subject, body=body, provider_id=provider_id, provider_name=provider_name,
    )
    return _serialize_msg(msg)


async def get_messages(user_id: str) -> list[dict]:
    msgs = await db_get_messages(user_id)
    return [_serialize_msg(m) for m in msgs]


async def get_message_by_id(message_id: str, user_id: str) -> Optional[dict]:
    msg = await db_get_message_by_id(message_id, user_id)
    return _serialize_msg(msg) if msg else None


async def reply_to_message(message_id: str, reply_body: str) -> Optional[dict]:
    msg = await db_reply_to_message(message_id, reply_body)
    return _serialize_msg(msg) if msg else None


async def get_message_by_id_internal(message_id: str) -> Optional[dict]:
    msg = await db_get_message_by_id_internal(message_id)
    return _serialize_msg(msg) if msg else None
