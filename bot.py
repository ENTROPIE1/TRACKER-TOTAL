import telebot
from telebot import types
from openai import OpenAI
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
from database import init_db, ensure_user, set_language, get_user

init_db()

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    user, is_new = ensure_user(message.from_user)
    if is_new:
        bot.send_message(message.chat.id, 'Welcome! 100 bonus credits added.')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Русский'), types.KeyboardButton('English'))
    msg = bot.send_message(
        message.chat.id,
        'Choose language / Выберите язык',
        reply_markup=markup,
    )
    bot.register_next_step_handler(msg, process_lang)


def process_lang(message):
    lang = 'ru' if 'Рус' in message.text else 'en'
    set_language(message.from_user.id, lang)
    bot.send_message(message.chat.id, 'Language saved.')


@bot.message_handler(commands=['profile'])
def profile(message):
    user = get_user(message.from_user.id)
    if not user:
        bot.reply_to(message, 'Send /start first.')
        return
    lang = 'Русский' if user['lang'] == 'ru' else 'English'
    text = f"Balance: {user['balance']}\nLanguage: {lang}"
    bot.reply_to(message, text)

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
