import os
import datetime
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Flask Server (Render ke liye zaroori hai) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Pandey Je Bot Ekdum Mast Chal Raha Hai!"

def run_flask():
    # Render default port 10000 ya 5000 use karta hai
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# --- Bot ki Settings ---
TOKEN = os.getenv("TOKEN")
BOT_NAME = "Pandey Je"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"Aur {user} bhai, kya haal chaal? 🙏\n\n"
        f"Main hoon **{BOT_NAME}**, tera bhai. Jo bhi baat karni hai, bindass bol. "
        "Tera bhai hamesha hazir hai! 😎",
        parse_mode='Markdown'
    )

# Chatting ka andaaz (Desi Style)
async def chat_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user.first_name

    if any(word in text for word in ["kaise ho", "kya haal", "how are you"]):
        reply = f"Main toh ekdum jhakaas hoon {user}! Tu bata, ghar pe sab thik-thaak?"
    
    elif any(word in text for word in ["naam", "who are you", "tera naam"]):
        reply = f"Arre bhool gaye kya? Main tera apna **{BOT_NAME}**! 😎"

    elif any(word in text for word in ["thik", "badhiya", "mast", "fine"]):
        reply = "Sunkar achha laga bhai! Aur bata, Pandey Je teri kya seva kar sakta hai?"

    elif "time" in text or "baj rahe" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        reply = f"Bhai, abhi ghadi mein {now} ho rahe hain."

    elif any(word in text for word in ["bye", "chalta hu", "tata"]):
        reply = f"Itni jaldi? Chal thik hai {user} bhai, apna khayal rakhna. Milte hain! 👋"

    else:
        reply = f"Dekh {user} bhai, teri baat sunkar achha laga, par Pandey Je ko abhi iska jawab nahi pata. Kuch aur baat karein?"

    await update.message.reply_text(reply)

def main():
    if not TOKEN:
        print("Error: TOKEN nahi mila! Render settings check karein.")
        return

    # Application setup
    application = Application.builder().token(TOKEN).build()

    # Commands aur Messages add karna
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_logic))

    print(f"{BOT_NAME} startup complete...")
    application.run_polling()

if __name__ == '__main__':
    # Flask ko alag thread mein chalana
    Thread(target=run_flask).start()
    # Bot ko start karna
    main()
