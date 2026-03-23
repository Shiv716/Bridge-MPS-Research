from __future__ import annotations
"""
Bridge – Database Layer
Async PostgreSQL via databases + asyncpg.
Tables: users, sessions, invite_tokens, reset_tokens.
"""

import os
import databases

DATABASE_URL = os.environ.get("DATABASE_URL", "")

# Neon requires SSL
if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require" if "?" not in DATABASE_URL else "&sslmode=require"

database = databases.Database(DATABASE_URL) if DATABASE_URL else None


# ─── Schema ───────────────────────────────────────────────────────────

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL DEFAULT '',
    firm TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL DEFAULT 'adviser',
    password_hash TEXT,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS invite_tokens (
    token TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    created_by TEXT REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS reset_tokens (
    token TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    used BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_invite_tokens_email ON invite_tokens(email);
CREATE INDEX IF NOT EXISTS idx_reset_tokens_user ON reset_tokens(user_id);

CREATE TABLE IF NOT EXISTS user_activity (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_type TEXT NOT NULL,
    event_data JSONB DEFAULT '{}',
    page TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_activity_user ON user_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_activity_type ON user_activity(event_type);
CREATE INDEX IF NOT EXISTS idx_activity_created ON user_activity(created_at);

CREATE TABLE IF NOT EXISTS user_preferences (
    user_id TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    preferences JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_email TEXT NOT NULL DEFAULT '',
    provider_id TEXT NOT NULL,
    provider_name TEXT NOT NULL DEFAULT '',
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_subs_user ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subs_provider ON subscriptions(provider_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_subs_user_provider ON subscriptions(user_id, provider_id) WHERE active = TRUE;

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_name TEXT NOT NULL DEFAULT '',
    user_firm TEXT NOT NULL DEFAULT '',
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    provider_id TEXT,
    provider_name TEXT,
    status TEXT NOT NULL DEFAULT 'sent',
    reply TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    replied_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS message_replies (
    id TEXT PRIMARY KEY,
    message_id TEXT NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    body TEXT NOT NULL,
    from_name TEXT NOT NULL DEFAULT 'Bridge Research',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_user ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_replies_message ON message_replies(message_id);
"""


async def init_db():
    """Connect and create tables."""
    if not database:
        print("WARNING: DATABASE_URL not set — auth will not work")
        return
    await database.connect()
    # Execute schema statements one at a time
    for statement in SCHEMA_SQL.strip().split(";"):
        statement = statement.strip()
        if statement:
            await database.execute(statement)
    print("Bridge DB: Connected and schema ready")


async def close_db():
    """Disconnect."""
    if database and database.is_connected:
        await database.disconnect()


# ─── User Queries ─────────────────────────────────────────────────────

async def create_user(*, user_id: str, email: str, name: str, firm: str, role: str = "adviser", password_hash: str = None) -> dict:
    await database.execute(
        "INSERT INTO users (id, email, name, firm, role, password_hash) VALUES (:id, :email, :name, :firm, :role, :pw)",
        {"id": user_id, "email": email.lower().strip(), "name": name, "firm": firm, "role": role, "pw": password_hash},
    )
    return await get_user_by_email(email)


async def get_user_by_email(email: str) -> dict | None:
    row = await database.fetch_one("SELECT * FROM users WHERE email = :email", {"email": email.lower().strip()})
    return dict(row._mapping) if row else None


async def get_user_by_id(user_id: str) -> dict | None:
    row = await database.fetch_one("SELECT * FROM users WHERE id = :id", {"id": user_id})
    return dict(row._mapping) if row else None


async def set_user_password(user_id: str, password_hash: str):
    await database.execute(
        "UPDATE users SET password_hash = :pw, email_verified = TRUE, updated_at = NOW() WHERE id = :id",
        {"pw": password_hash, "id": user_id},
    )


async def list_all_users() -> list[dict]:
    rows = await database.fetch_all("SELECT id, email, name, firm, role, email_verified, created_at FROM users ORDER BY created_at DESC")
    return [dict(r._mapping) for r in rows]


async def delete_user(user_id: str):
    await database.execute("DELETE FROM users WHERE id = :id", {"id": user_id})


# ─── Session Queries ──────────────────────────────────────────────────

async def create_session_row(token: str, user_id: str, expires_at):
    await database.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (:token, :uid, :exp)",
        {"token": token, "uid": user_id, "exp": expires_at},
    )


async def get_session_row(token: str) -> dict | None:
    row = await database.fetch_one(
        "SELECT s.*, u.email, u.name, u.firm, u.role FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token = :token AND s.expires_at > NOW()",
        {"token": token},
    )
    return dict(row._mapping) if row else None


async def delete_session_row(token: str):
    await database.execute("DELETE FROM sessions WHERE token = :token", {"token": token})


async def cleanup_expired_sessions():
    await database.execute("DELETE FROM sessions WHERE expires_at < NOW()")


# ─── Invite Token Queries ─────────────────────────────────────────────

async def create_invite_token(token: str, email: str, created_by: str, expires_at):
    await database.execute(
        "INSERT INTO invite_tokens (token, email, created_by, expires_at) VALUES (:token, :email, :by, :exp)",
        {"token": token, "email": email.lower().strip(), "by": created_by, "exp": expires_at},
    )


async def get_invite_token(token: str) -> dict | None:
    row = await database.fetch_one(
        "SELECT * FROM invite_tokens WHERE token = :token AND used = FALSE AND expires_at > NOW()",
        {"token": token},
    )
    return dict(row._mapping) if row else None


async def mark_invite_used(token: str):
    await database.execute("UPDATE invite_tokens SET used = TRUE WHERE token = :token", {"token": token})


# ─── Reset Token Queries ──────────────────────────────────────────────

async def create_reset_token(token: str, user_id: str, expires_at):
    await database.execute(
        "INSERT INTO reset_tokens (token, user_id, expires_at) VALUES (:token, :uid, :exp)",
        {"token": token, "uid": user_id, "exp": expires_at},
    )


async def get_reset_token(token: str) -> dict | None:
    row = await database.fetch_one(
        "SELECT * FROM reset_tokens WHERE token = :token AND used = FALSE AND expires_at > NOW()",
        {"token": token},
    )
    return dict(row._mapping) if row else None


async def mark_reset_used(token: str):
    await database.execute("UPDATE reset_tokens SET used = TRUE WHERE token = :token", {"token": token})


# ─── Activity Tracking Queries ────────────────────────────────────────

async def log_activity(*, activity_id: str, user_id: str, event_type: str, event_data: dict = None, page: str = None):
    import json
    await database.execute(
        "INSERT INTO user_activity (id, user_id, event_type, event_data, page) VALUES (:id, :uid, :type, :data, :page)",
        {"id": activity_id, "uid": user_id, "type": event_type, "data": json.dumps(event_data or {}), "page": page},
    )


async def get_activity_for_user(user_id: str, limit: int = 50) -> list[dict]:
    rows = await database.fetch_all(
        "SELECT * FROM user_activity WHERE user_id = :uid ORDER BY created_at DESC LIMIT :lim",
        {"uid": user_id, "lim": limit},
    )
    return [dict(r._mapping) for r in rows]


async def get_recent_activity(limit: int = 100) -> list[dict]:
    rows = await database.fetch_all(
        "SELECT a.*, u.name, u.email, u.firm FROM user_activity a JOIN users u ON a.user_id = u.id ORDER BY a.created_at DESC LIMIT :lim",
        {"lim": limit},
    )
    return [dict(r._mapping) for r in rows]


async def get_activity_stats() -> dict:
    """Get summary stats for the admin dashboard."""
    # Active users (logged in within last 7 days)
    active = await database.fetch_one(
        "SELECT COUNT(DISTINCT user_id) as count FROM user_activity WHERE event_type = 'login' AND created_at > NOW() - INTERVAL '7 days'"
    )
    # Total logins last 30 days
    logins = await database.fetch_one(
        "SELECT COUNT(*) as count FROM user_activity WHERE event_type = 'login' AND created_at > NOW() - INTERVAL '30 days'"
    )
    # Total page views last 30 days
    views = await database.fetch_one(
        "SELECT COUNT(*) as count FROM user_activity WHERE event_type = 'page_view' AND created_at > NOW() - INTERVAL '30 days'"
    )
    # Most viewed pages
    top_pages = await database.fetch_all(
        "SELECT page, COUNT(*) as count FROM user_activity WHERE event_type = 'page_view' AND created_at > NOW() - INTERVAL '30 days' AND page IS NOT NULL GROUP BY page ORDER BY count DESC LIMIT 10"
    )
    # Feature usage
    features = await database.fetch_all(
        "SELECT event_type, COUNT(*) as count FROM user_activity WHERE event_type NOT IN ('login', 'page_view', 'session_heartbeat') AND created_at > NOW() - INTERVAL '30 days' GROUP BY event_type ORDER BY count DESC"
    )
    return {
        "active_users_7d": active["count"] if active else 0,
        "logins_30d": logins["count"] if logins else 0,
        "page_views_30d": views["count"] if views else 0,
        "top_pages": [dict(r._mapping) for r in top_pages],
        "feature_usage": [dict(r._mapping) for r in features],
    }

# ─── Preferences Queries ──────────────────────────────────────────────

async def db_get_preferences(user_id: str) -> dict | None:
    row = await database.fetch_one("SELECT preferences FROM user_preferences WHERE user_id = :uid", {"uid": user_id})
    if not row:
        return None
    val = row["preferences"]
    if isinstance(val, str):
        import json
        return json.loads(val)
    return val


async def db_upsert_preferences(user_id: str, prefs: dict):
    import json
    prefs_json = json.dumps(prefs)
    # Try update first, then insert
    result = await database.execute(
        "UPDATE user_preferences SET preferences = :prefs, updated_at = NOW() WHERE user_id = :uid",
        {"prefs": prefs_json, "uid": user_id},
    )
    # Check if row existed
    row = await database.fetch_one("SELECT 1 FROM user_preferences WHERE user_id = :uid", {"uid": user_id})
    if not row:
        await database.execute(
            "INSERT INTO user_preferences (user_id, preferences) VALUES (:uid, :prefs)",
            {"uid": user_id, "prefs": prefs_json},
        )


# ─── Subscription Queries ─────────────────────────────────────────────

async def db_subscribe(*, sub_id: str, user_id: str, user_email: str, provider_id: str, provider_name: str) -> dict:
    # Check existing active
    row = await database.fetch_one(
        "SELECT * FROM subscriptions WHERE user_id = :uid AND provider_id = :pid AND active = TRUE",
        {"uid": user_id, "pid": provider_id},
    )
    if row:
        return dict(row._mapping)
    await database.execute(
        "INSERT INTO subscriptions (id, user_id, user_email, provider_id, provider_name) VALUES (:id, :uid, :email, :pid, :pname)",
        {"id": sub_id, "uid": user_id, "email": user_email, "pid": provider_id, "pname": provider_name},
    )
    row = await database.fetch_one("SELECT * FROM subscriptions WHERE id = :id", {"id": sub_id})
    return dict(row._mapping)


async def db_unsubscribe(user_id: str, provider_id: str) -> bool:
    result = await database.execute(
        "UPDATE subscriptions SET active = FALSE WHERE user_id = :uid AND provider_id = :pid AND active = TRUE",
        {"uid": user_id, "pid": provider_id},
    )
    return True


async def db_get_subscriptions(user_id: str) -> list[dict]:
    rows = await database.fetch_all(
        "SELECT * FROM subscriptions WHERE user_id = :uid AND active = TRUE ORDER BY created_at DESC",
        {"uid": user_id},
    )
    return [dict(r._mapping) for r in rows]


async def db_is_subscribed(user_id: str, provider_id: str) -> bool:
    row = await database.fetch_one(
        "SELECT 1 FROM subscriptions WHERE user_id = :uid AND provider_id = :pid AND active = TRUE",
        {"uid": user_id, "pid": provider_id},
    )
    return row is not None


async def db_notify_subscribers(provider_id: str) -> list[dict]:
    rows = await database.fetch_all(
        "SELECT * FROM subscriptions WHERE provider_id = :pid AND active = TRUE",
        {"pid": provider_id},
    )
    return [dict(r._mapping) for r in rows]


# ─── Message Queries ──────────────────────────────────────────────────

async def db_send_message(*, msg_id: str, user_id: str, user_name: str, user_firm: str, subject: str, body: str, provider_id: str = None, provider_name: str = None) -> dict:
    await database.execute(
        """INSERT INTO messages (id, user_id, user_name, user_firm, subject, body, provider_id, provider_name)
        VALUES (:id, :uid, :uname, :ufirm, :subj, :body, :pid, :pname)""",
        {"id": msg_id, "uid": user_id, "uname": user_name, "ufirm": user_firm, "subj": subject, "body": body, "pid": provider_id, "pname": provider_name},
    )
    return await db_get_message_by_id_internal(msg_id)


async def db_get_messages(user_id: str) -> list[dict]:
    rows = await database.fetch_all(
        "SELECT * FROM messages WHERE user_id = :uid ORDER BY created_at DESC",
        {"uid": user_id},
    )
    msgs = []
    for r in rows:
        m = dict(r._mapping)
        replies = await database.fetch_all(
            "SELECT * FROM message_replies WHERE message_id = :mid ORDER BY created_at ASC",
            {"mid": m["id"]},
        )
        m["replies"] = [dict(rep._mapping) for rep in replies]
        msgs.append(m)
    return msgs


async def db_get_message_by_id(message_id: str, user_id: str) -> dict | None:
    row = await database.fetch_one(
        "SELECT * FROM messages WHERE id = :mid AND user_id = :uid",
        {"mid": message_id, "uid": user_id},
    )
    if not row:
        return None
    m = dict(row._mapping)
    replies = await database.fetch_all(
        "SELECT * FROM message_replies WHERE message_id = :mid ORDER BY created_at ASC",
        {"mid": m["id"]},
    )
    m["replies"] = [dict(rep._mapping) for rep in replies]
    return m


async def db_get_message_by_id_internal(message_id: str) -> dict | None:
    row = await database.fetch_one("SELECT * FROM messages WHERE id = :mid", {"mid": message_id})
    if not row:
        return None
    m = dict(row._mapping)
    replies = await database.fetch_all(
        "SELECT * FROM message_replies WHERE message_id = :mid ORDER BY created_at ASC",
        {"mid": m["id"]},
    )
    m["replies"] = [dict(rep._mapping) for rep in replies]
    return m


async def db_reply_to_message(message_id: str, reply_body: str) -> dict | None:
    msg = await db_get_message_by_id_internal(message_id)
    if not msg:
        return None
    import secrets
    reply_id = f"rep-{secrets.token_hex(6)}"
    await database.execute(
        "INSERT INTO message_replies (id, message_id, body) VALUES (:id, :mid, :body)",
        {"id": reply_id, "mid": message_id, "body": reply_body},
    )
    await database.execute(
        "UPDATE messages SET status = 'replied', reply = :reply, replied_at = NOW() WHERE id = :mid",
        {"reply": reply_body, "mid": message_id},
    )
    return await db_get_message_by_id_internal(message_id)
