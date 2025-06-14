# TRACKER-TOTAL

This project contains a simple session tracker with message storage.

## Features
- Sessions table stores user sessions with start/end timestamps and a summary.
- Messages table stores messages linked to a session.
- Command line interface:
  - `start_session <telegram_id>` starts a new session.
  - `message <session_id> <telegram_id> <text>` saves a message.
  - `end_session <session_id>` ends a session and stores a summary.
  - `latest_summary <telegram_id>` prints the last session summary.

The summary is generated from the concatenated session messages and trimmed
for brevity.

Run the tests with `python -m unittest`.
