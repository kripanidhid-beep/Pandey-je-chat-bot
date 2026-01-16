import os
import telebot
from flask import Flask
import threading

# Render se Token uthana
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Namaste! Pandey Ji ka normal bot ab chalu hai. Kaise hain aap?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_text = message.text.lower()
    
    # Normal replies yahan set karein
    if "kaise ho" in user_text:
        bot.reply_to(message, "Main badhiya hoon bhai, aap batao!")
    elif "kaun ho" in user_text:
        bot.reply_to(message, "Main Pandey Ji ka chota sa chatbot hoon.")
    elif "hi" in user_text or "hello" in user_text:
        bot.reply_to(message, "Hello! Kaise madad karoon?")
    else:
        bot.reply_to(message, "Sahi hai! Main abhi seekh raha hoon.")

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    print("Bot is starting...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    
