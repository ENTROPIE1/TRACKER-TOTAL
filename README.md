## Environment variables

- `TELEGRAM_TOKEN` – bot token from @BotFather
- `OPENAI_KEY` – API key for OpenAI
- `OPENAI_MODEL` – model name, defaults to `gpt-4o-mini`
- `OPENAI_BASE_URL` – base URL for the API; defaults to
  `https://api.proxyapi.ru/openai/v1` for regions blocked by OpenAI
- `HISTORY_LIMIT` – how many messages to keep in history

When you send `/start` the bot will ask you to choose a language. The choice is stored per user and controls the interface and system prompt. English and Russian are available by default, but more languages can be added later.
