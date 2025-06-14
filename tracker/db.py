import sqlite3
from datetime import datetime
from typing import List, Optional

from . import summarizer


class Database:
    def __init__(self, path: str = "tracker.db"):
        self.conn = sqlite3.connect(path)
        self._setup()

    def _setup(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                start_ts TEXT NOT NULL,
                end_ts TEXT,
                summary TEXT
            )
            """
        )
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL REFERENCES sessions(id),
                telegram_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                ts TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    # Session management
    def start_session(self, telegram_id: int) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO sessions (telegram_id, start_ts) VALUES (?, ?)",
            (telegram_id, datetime.utcnow().isoformat()),
        )
        self.conn.commit()
        return cur.lastrowid

    def end_session(self, session_id: int) -> str:
        messages = [row[0] for row in self.conn.execute(
            "SELECT content FROM messages WHERE session_id = ? ORDER BY ts",
            (session_id,),
        ).fetchall()]
        summary = summarizer.summarize(messages)
        self.conn.execute(
            "UPDATE sessions SET end_ts = ?, summary = ? WHERE id = ?",
            (datetime.utcnow().isoformat(), summary, session_id),
        )
        self.conn.commit()
        return summary

    def latest_session_summary(self, telegram_id: int) -> Optional[str]:
        row = self.conn.execute(
            "SELECT summary FROM sessions WHERE telegram_id = ? AND summary IS NOT NULL ORDER BY start_ts DESC LIMIT 1",
            (telegram_id,),
        ).fetchone()
        return row[0] if row else None

    # Message storage
    def store_message(self, session_id: int, telegram_id: int, content: str) -> None:
        self.conn.execute(
            "INSERT INTO messages (session_id, telegram_id, content, ts) VALUES (?, ?, ?, ?)",
            (session_id, telegram_id, content, datetime.utcnow().isoformat()),
        )
        self.conn.commit()

    def get_session_messages(self, session_id: int) -> List[str]:
        return [row[0] for row in self.conn.execute(
            "SELECT content FROM messages WHERE session_id = ? ORDER BY ts",
            (session_id,),
        ).fetchall()]
