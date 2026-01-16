import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# API Keys setup
TOKEN = os.environ.get('TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini AI Configure karna
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste! Main Pandey Je ka AI assistant hoon. Ab aap mujhse kuch bhi pooch sakte hain! 😊")

# Ye part har message ka AI se jawab dilwayega
@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Thoda bhatak gaya hoon, phir se poochiye!")

@app.route('/')
def home():
    return "AI Bot is Running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot is starting...")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

