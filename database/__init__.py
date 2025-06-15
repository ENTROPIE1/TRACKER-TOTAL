import sqlite3
from pathlib import Path
from config import DB_PATH

SCHEMA_PATH = Path(__file__).with_name('schema.sql')

def init_db():
    """Create tables if database is empty."""
    db_file = Path(DB_PATH)
    conn = sqlite3.connect(db_file)
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_PATH)
