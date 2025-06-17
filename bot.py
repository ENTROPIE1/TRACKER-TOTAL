import telebot
from telebot import types
from openai import OpenAI
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
from database import init_db, ensure_user, set_language, get_user

# Supported languages and translations for bot messages.  Extend this dict to
# add new languages.
MESSAGES = {
    'en': {
        'welcome': 'Welcome! 100 bonus credits added.',
        'choose_lang': 'Choose language',
        'lang_saved': 'Language saved.',
        'profile': 'Balance: {balance}\nLanguage: {lang}',
        'send_start': 'Send /start first.',
        'change_lang': 'Change language',
    },
    'ru': {
        'welcome': 'Добро пожаловать! 100 бонусных кредитов начислено.',
        'choose_lang': 'Выберите язык',
        'lang_saved': 'Язык сохранён.',
        'profile': 'Баланс: {balance}\nЯзык: {lang}',
        'send_start': 'Сначала отправьте /start.',
        'change_lang': 'Сменить язык',
    },
}

# Human readable titles of languages for buttons. Keys correspond to language
# codes in MESSAGES. Modify this dict to expose additional languages in the
# UI.
LANG_BUTTONS = {
    'en': 'English',
    'ru': 'Русский',
}


def tr(lang: str, key: str) -> str:
    """Return translated message for language/code pair."""
    return MESSAGES.get(lang, MESSAGES['en']).get(key, key)

init_db()

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    user, is_new = ensure_user(message.from_user)
    if is_new:
        # Show welcome text in both languages since the user has not chosen
        # their preferred language yet.
        welcome = f"{tr('en', 'welcome')} / {tr('ru', 'welcome')}"
        bot.send_message(message.chat.id, welcome)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for code, title in LANG_BUTTONS.items():
        markup.add(types.KeyboardButton(title))
    prompt = f"{tr('en', 'choose_lang')} / {tr('ru', 'choose_lang')}"
    msg = bot.send_message(message.chat.id, prompt, reply_markup=markup)

    bot.register_next_step_handler(msg, process_lang)


def process_lang(message):
    # Map button title back to language code, default to English.
    reverse = {v: k for k, v in LANG_BUTTONS.items()}
    lang = reverse.get(message.text, 'en')
    set_language(message.from_user.id, lang)
    bot.send_message(message.chat.id, tr(lang, 'lang_saved'))



@bot.message_handler(commands=['profile'])
def profile(message):
    user = get_user(message.from_user.id)
    if not user:
        bot.reply_to(message, tr('en', 'send_start'))
        return
    lang = user['lang']
    lang_title = LANG_BUTTONS.get(lang, lang)
    text = tr(lang, 'profile').format(balance=user['balance'], lang=lang_title)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(tr(lang, 'change_lang'), callback_data='change_lang'))
    bot.reply_to(message, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'change_lang')
def change_lang(call):
    user = get_user(call.from_user.id)
    lang = user['lang'] if user else 'en'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for code, title in LANG_BUTTONS.items():
        markup.add(types.KeyboardButton(title))
    msg = bot.send_message(call.message.chat.id, tr(lang, 'choose_lang'), reply_markup=markup)
    bot.register_next_step_handler(msg, process_lang)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    chat_completion = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': message.text}],
    )
    reply = chat_completion.choices[0].message.content
    bot.reply_to(message, reply)

if __name__ == '__main__':
    bot.infinity_polling()
