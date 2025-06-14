# TRACKER-TOTAL

TRACKER-TOTAL is an experimental conversation tracker. It stores every
message in a session and keeps a lightweight summary so that context can be
reloaded later. The following sections describe the database tables, commands,
and environment variables involved in the session logic.

## Database tables

- **sessions** – records the `session_id`, when it started, when it ended and
  whether it is active.
- **messages** – stores each message along with its `session_id`, timestamp and
  role (`user` or `assistant`).
- **summaries** – for every session we store a compact text summary that can be
  used to prime future conversations.
- **commands** – optional log of special commands executed while a session is
  running.

## Starting a session

Run the `start` command to open a new session. A row is created in the
`sessions` table with the current timestamp and the session becomes the active
context for new messages.

## Ending a session

Use the `end` command when you want to close the current session. This marks
its `ended_at` field and stops messages from being appended. The final summary
is generated and stored in the `summaries` table.

## How summaries influence conversations

When a new session begins, the system checks for an existing summary for the
same user or project. If one exists, the text is injected into the initial
prompt so the assistant is aware of prior discussion without loading the full
message history.

## Additional commands

- `list` – show all stored sessions
- `show <id>` – display the messages and summary for a specific session
- `summary <id>` – regenerate a summary for the given session if needed

## Environment variables and settings

| Variable | Description | Default |
|----------|-------------|---------|
| `TRACKER_DB_PATH` | Path to the SQLite database file. | `./data/tracker.db` |
| `TRACKER_SESSION_TIMEOUT` | Number of idle minutes before a session is auto-ended. | `30` |
| `TRACKER_SUMMARIZER` | Which summarization model or script to use. | `default` |
| `TRACKER_LOG_LEVEL` | Verbosity of logging (`info`, `debug`, etc.). | `info` |

These settings customize how sessions are stored, when they expire, and how
summaries are produced.
