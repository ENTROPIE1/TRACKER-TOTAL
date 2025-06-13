# DOMINA SUPREMA Bot

Минимальный Telegram-бот, поддерживающий диалог через OpenAI, ведение краткой истории сообщений в SQLite и напоминания при бездействии пользователя.

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt --break-system-packages
   ```
2. Скопируйте `.env.example` в `.env` и заполните значения.
3. Запустите бот:
   ```bash
   python bot.py
   ```

### Переменные окружения

```
TELEGRAM_TOKEN=...  # токен бота
OPENAI_KEY=...      # ключ OpenAI
OPENAI_MODEL=gpt-4o-mini
HISTORY_LIMIT=20    # сколько пар сообщений хранить
IDLE_TIMEOUT=3600   # через сколько секунд напоминать о молчании
```
