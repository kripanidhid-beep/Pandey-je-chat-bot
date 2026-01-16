import os
import telebot
from flask import Flask
import threading

# Environment variables se data nikalna
TOKEN = os.environ.get('TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')
app = Flask(__name__)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Namaste! Pandey Je Chat Bot ab zinda hai. 🙏")

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Flask ko alag thread mein chalana
    threading.Thread(target=run_flask).start()
    # Bot ko start karna
    print("Bot is starting...")
    bot.infinity_polling()
    
