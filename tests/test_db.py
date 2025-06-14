import os
import unittest
from tracker.db import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test.db'
        # remove file if exists
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.db = Database(self.db_path)

    def tearDown(self):
        self.db.conn.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_session_flow(self):
        sid = self.db.start_session(123)
        self.db.store_message(sid, 123, 'hello')
        self.db.store_message(sid, 123, 'world')
        summary = self.db.end_session(sid)
        self.assertTrue(summary)
        self.assertEqual(self.db.latest_session_summary(123), summary)
        msgs = self.db.get_session_messages(sid)
        self.assertEqual(len(msgs), 2)


if __name__ == '__main__':
    unittest.main()
