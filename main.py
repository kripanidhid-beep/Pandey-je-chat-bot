import os
import telebot
import google.generativeai as genai
from flask import Flask
import threading

# Render ke environment variables se data uthana
TOKEN = os.environ.get('TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini Setup
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste! Pandey Je AI ab taiyar hai. Kuch bhi poochen!")

@bot.message_handler(func=lambda message: True)
def ai_reply(message):
    try:
        # AI se jawab mangna
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "AI connect nahi ho paa raha, Gemini Key check karein.")

@app.route('/')
def home():
    return "Pandey Je Bot is Live!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    # Conflict se bachne ke liye infinity polling
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    
