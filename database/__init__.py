import sqlite3
from pathlib import Path
from config import DB_PATH

SCHEMA_PATH = Path(__file__).with_name('schema.sql')

def init_db():
    """Initialize database with schema if it doesn't exist."""
    db_file = Path(DB_PATH)
    first_run = not db_file.exists()
    conn = sqlite3.connect(db_file)
    if first_run:
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)


def ensure_user(tg_user):
    """Return dict with user info, creating record if needed."""
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE tg_id=?", (tg_user.id,))
    row = cur.fetchone()
    is_new = False
    if row is None:
        cur.execute(
            "INSERT INTO users (tg_id, username, first_name, last_name)"
            " VALUES (?,?,?,?)",
            (tg_user.id, tg_user.username, tg_user.first_name, tg_user.last_name),
        )
        user_id = cur.lastrowid
        # grant welcome bonus
        cur.execute("UPDATE users SET balance = balance + 100 WHERE id=?", (user_id,))
        cur.execute(
            "INSERT INTO ledger (user_id, delta, ref_type) VALUES (?,?,'bonus')",
            (user_id, 100),
        )
        conn.commit()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        is_new = True
    else:
        # update name info
        cur.execute(
            "UPDATE users SET username=?, first_name=?, last_name=? WHERE tg_id=?",
            (tg_user.username, tg_user.first_name, tg_user.last_name, tg_user.id),
        )
        conn.commit()
    user = dict(row)
    conn.close()
    return user, is_new


def set_language(tg_id, lang):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET lang=? WHERE tg_id=?", (lang, tg_id))
    conn.commit()
    conn.close()


def get_user(tg_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None
