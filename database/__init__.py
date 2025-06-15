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
