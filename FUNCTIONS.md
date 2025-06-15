# Описание функций `bot.py`

| Функция | Назначение |
|---------|------------|
| `init_db()` | Инициализация базы данных и создание таблиц. |
| `get_current_session_id(telegram_id)` | Возвращает идентификатор активной сессии. |
| `start_session(telegram_id)` | Создаёт новую сессию и отмечает её активной для пользователя. |
| `end_session(telegram_id)` | Завершает текущую сессию, отправляет диалог на summarization и сохраняет конспект. |
| `summarize_session(dialog)` | Делает краткий конспект диалога через OpenAI. |
| `save_msg(session_id, telegram_id, role, text)` | Сохраняет сообщение в таблицу `messages`. |
| `update_last(telegram_id, user=False, bot=False)` | Обновляет время последней активности пользователя или бота. |
| `get_user_lang(telegram_id)` | Возвращает язык интерфейса пользователя. |
| `set_user_lang(telegram_id, lang)` | Сохраняет выбранный пользователем язык. |
| `fetch_history(telegram_id)` | Возвращает системный промт, конспект прошлой сессии и историю текущей. |
| `handle_start(msg)` | Регистрирует пользователя и приветствует его. |
| `handle_language(call)` | Обработчик выбора языка из кнопок. |
| `handle_start_session(msg)` | Обработчик команды `/start_session`. |
| `handle_end_session(msg)` | Обработчик команды `/end_session`. |
| `handle_text(msg)` | Основной обработчик входящих сообщений. |
