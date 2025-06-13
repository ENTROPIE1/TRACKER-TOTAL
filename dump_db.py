import sqlite3
import sys

DB_PATH = 'bot.db'


def dump_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    print('Users:')
    for row in conn.execute('SELECT telegram_id, last_user_ts, last_bot_ts FROM users ORDER BY telegram_id'):
        print(row)
    print('\nMessages:')
    for row in conn.execute('SELECT id, telegram_id, role, content, ts FROM messages ORDER BY id'):
        print(row)
    conn.close()


if __name__ == '__main__':
    db_path = sys.argv[1] if len(sys.argv) > 1 else DB_PATH
    dump_db(db_path)
