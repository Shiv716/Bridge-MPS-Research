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
