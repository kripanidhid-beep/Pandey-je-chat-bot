import os
import datetime
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Server setup for Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Pandey Je Bot is LIVE and Rocking! 🔥"

def run_flask():
    port = int(os.environ.get('PORT', 10000)) 
    app.run(host='0.0.0.0', port=port)


# --- Bot Configurations ---
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID") # Render Dashboard me apna ID jarur dalein
BOT_NAME = "Pandey Je"

# 1. /start command logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    msg = (f"Namaste {user} bhai! 🙏\n\n"
           f"Main hoon **{BOT_NAME}**. Main messages par reaction bhi deta hoon "
           "aur aapki baaton ka desi jawab bhi. Bolo, kya seva karein? 😎")
    await update.message.reply_text(msg, parse_mode='Markdown')

# 2. Group me welcome message
async def welcome_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text(f"Pranaam dosto! 🙏 Main hoon **{BOT_NAME}**. Ab is group mein rounak aayegi! 🔥")

# 3. Admin Command: Kisi bhi group/chat me message bhejna
# Use: /sendto [ID] [Message]
async def send_to_anywhere(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) == str(ADMIN_ID):
        if len(context.args) < 2:
            await update.message.reply_text("Format: `/sendto ID message`", parse_mode='Markdown')
            return
        target_id = context.args[0]
        text = " ".join(context.args[1:])
        try:
            await context.bot.send_message(chat_id=target_id, text=text)
            await update.message.reply_text("Message bhej diya gaya hai! ✅")
        except Exception as e:
            await update.message.reply_text(f"Nahi gaya bhai! Error: {e}")
    else:
        await update.message.reply_text("Bhai ye power sirf Admin ke paas hai! ❌")

# 4. Main Chat Logic (Reactions + Replies + Admin Alert)
async def handle_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    msg_id = update.message.message_id
    chat_type = update.message.chat.type

    # A. Automatic Reaction (Emoji lagana)
    try:
        # Aap "👍" badal kar "❤️" ya "🔥" bhi kar sakte hain
        await context.bot.set_message_reaction(
            chat_id=chat_id,
            message_id=msg_id,
            reaction=[{"type": "emoji", "emoji": "👍"}]
        )
    except:
        pass # Kuch bots/chats me reaction allow nahi hote

    # B. Admin Alert (Koi personal message kare to aapko pta chale)
    if chat_type == "private" and str(user_id) != str(ADMIN_ID):
        alert = (f"📩 **Naya Message Aaya!**\n"
                 f"👤 Naam: {user}\n"
                 f"🆔 ID: `{user_id}`\n"
                 f"💬 Message: {text}")
        await context.bot.send_message(chat_id=ADMIN_ID, text=alert, parse_mode='Markdown')

    # C. Desi Chat Replies
    text_l = text.lower()
    if any(x in text_l for x in ["kaise ho", "kya haal"]):
        await update.message.reply_text(f"Main jhakaas hoon {user} bhai! Tum sunao?")
    elif "pandey" in text_l:
        await update.message.reply_text("Bolo bhai, Pandey Je hazir hain! 👑")
    elif any(x in text_l for x in ["bye", "tata", "shubhratri"]):
        await update.message.reply_text("Chalo thik hai bhai, apna dhyan rakhna! 👋")

# --- Bot Startup ---
def main():
    if not TOKEN:
        print("Error: TOKEN missing!")
        return
    
    app_bot = Application.builder().token(TOKEN).build()

    # Handlers add karna
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("sendto", send_to_anywhere))
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_group))
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_all_messages))

    print(f"{BOT_NAME} start ho gaya...")
    app_bot.run_polling()

if __name__ == '__main__':
    # Flask ko alag thread mein chalana
    Thread(target=run_flask).start()
    # Bot ko start karna
    main()

