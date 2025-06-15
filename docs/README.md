# Tracker Total Bot

Minimal skeleton of a Telegram bot using pyTelegramBotAPI and OpenAI SDK.
The project ships with a SQLite schema providing users, sessions and
ledger bookkeeping triggers. On first `/start` the bot stores the user,
grants 100 bonus credits and asks to select a language. The `/profile`
command shows the stored balance and language.

## Setup
1. Copy `.env.example` to `.env` and fill in your keys.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the bot: `python bot.py`.

Database schema is located in `database/schema.sql`.
