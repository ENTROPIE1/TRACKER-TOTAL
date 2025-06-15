import telebot
from openai import OpenAI
from config import TELEGRAM_TOKEN, OPENAI_API_KEY
from database import init_db, get_connection

init_db()

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello! Send me a message and I will ask OpenAI.')

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
