-- Users table
CREATE TABLE users (
    id            INTEGER PRIMARY KEY,
    tg_id         INTEGER NOT NULL UNIQUE,
    username      TEXT,
    first_name    TEXT,
    last_name     TEXT,
    lang          TEXT NOT NULL DEFAULT 'ru',
    balance       INTEGER NOT NULL DEFAULT 0,
    is_admin      INTEGER NOT NULL DEFAULT 0,
    trial_granted INTEGER NOT NULL DEFAULT 0,
    created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at    DATETIME
);

-- Personas table
CREATE TABLE personas (
    id           INTEGER PRIMARY KEY,
    code         TEXT NOT NULL UNIQUE,
    title        TEXT NOT NULL,
    prompt       TEXT NOT NULL,
    temperature  REAL NOT NULL DEFAULT 0.9,
    is_active    INTEGER NOT NULL DEFAULT 1
);

-- Sessions table
CREATE TABLE sessions (
    id            INTEGER PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    persona_id    INTEGER REFERENCES personas(id),
    started_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at      DATETIME,
    credits_spent INTEGER NOT NULL DEFAULT 0,
    tokens_used   INTEGER NOT NULL DEFAULT 0,
    msg_count     INTEGER NOT NULL DEFAULT 0,
    summary       TEXT
);

-- Messages table
CREATE TABLE messages (
    id            INTEGER PRIMARY KEY,
    session_id    INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    sender_role   TEXT NOT NULL,
    content       TEXT NOT NULL,
    tokens        INTEGER NOT NULL,
    credits_cost  INTEGER NOT NULL,
    ts            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_messages_session_ts ON messages(session_id, ts);

-- Ledger table
CREATE TABLE ledger (
    id            INTEGER PRIMARY KEY,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id    INTEGER,
    message_id    INTEGER,
    delta         INTEGER NOT NULL,
    ref_type      TEXT NOT NULL,
    currency_amt  REAL,
    currency      TEXT,
    provider      TEXT,
    provider_txn  TEXT,
    ts            DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_ledger_user_ts   ON ledger(user_id, ts DESC);
CREATE INDEX idx_ledger_session   ON ledger(session_id);
CREATE INDEX idx_ledger_message   ON ledger(message_id);

-- Settings table
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    val TEXT NOT NULL
);

-- Trigger: bookkeeping on message insert
CREATE TRIGGER trg_messages_bookkeep
AFTER INSERT ON messages
BEGIN
    UPDATE users
    SET balance = balance - NEW.credits_cost
    WHERE id = (SELECT user_id FROM sessions WHERE id = NEW.session_id);

    UPDATE sessions
    SET tokens_used   = tokens_used   + NEW.tokens,
        credits_spent = credits_spent + NEW.credits_cost,
        msg_count     = msg_count     + 1
    WHERE id = NEW.session_id;

    INSERT INTO ledger (user_id, session_id, message_id,
                        delta, ref_type, ts)
    VALUES (
        (SELECT user_id FROM sessions WHERE id = NEW.session_id),
        NEW.session_id,
        NEW.id,
        -NEW.credits_cost,
        'message',
        CURRENT_TIMESTAMP
    );
END;
