import os
import sqlite3
import uuid

VAULT_KEY = os.getenv("VAULT_KEY", "changeme32charsecretkey!!!!!!!!")
DB_PATH = "vault.db"

def _conn():
    con = sqlite3.connect(DB_PATH)
    con.execute(f"PRAGMA key='{VAULT_KEY}'")
    return con

def init_vault():
    con = _conn()
    con.execute("""
        CREATE TABLE IF NOT EXISTS secrets (
            id TEXT PRIMARY KEY,
            owner TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT NOT NULL,
            scope TEXT NOT NULL DEFAULT '[]'
        )
    """)
    con.commit()
    con.close()

def store_secret(owner: str, value: str) -> str:
    record_id = str(uuid.uuid4())
    con = _conn()
    con.execute(
        "INSERT INTO secrets (id, owner, value) VALUES (?, ?, ?)",
        (record_id, owner, value)
    )
    con.commit()
    con.close()
    return record_id

def fetch_secret(record_id: str, owner: str) -> str | None:
    con = _conn()
    row = con.execute(
        "SELECT value FROM secrets WHERE id=? AND owner=?",
        (record_id, owner)
    ).fetchone()
    con.close()
    return row[0] if row else None

def delete_secret(record_id: str, owner: str) -> bool:
    con = _conn()
    cur = con.execute(
        "DELETE FROM secrets WHERE id=? AND owner=?",
        (record_id, owner)
    )
    con.commit()
    con.close()
    return cur.rowcount > 0

def create_user(username: str, hashed_password: str, scope: list[str]):
    import json
    con = _conn()
    con.execute(
        "INSERT INTO users (username, hashed_password, scope) VALUES (?, ?, ?)",
        (username, hashed_password, json.dumps(scope))
    )
    con.commit()
    con.close()

def get_user(username: str) -> dict | None:
    import json
    con = _conn()
    row = con.execute(
        "SELECT username, hashed_password, scope FROM users WHERE username=?",
        (username,)
    ).fetchone()
    con.close()
    if not row:
        return None
    return {"username": row[0], "hashed_password": row[1], "scope": json.loads(row[2])}
