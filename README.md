# DOMINA SUPREMA Bot

Минимальный Telegram-бот, поддерживающий диалог через OpenAI и хранение чатов по сессиям в SQLite.

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

### Команды
* `/start` — регистрация пользователя
* `/start_session` — начать новую сессию общения
* `/end_session` — завершить текущую сессию

### Переменные окружения

```
TELEGRAM_TOKEN=...  # токен бота
OPENAI_KEY=...      # ключ OpenAI
OPENAI_MODEL=gpt-4o-mini
HISTORY_LIMIT=20    # сколько пар сообщений хранить
```

### Просмотр базы
Для вывода содержимого SQLite выполните:
```bash
python dump_db.py
```

