import logging
import os
from threading import Thread
from flask import Flask
import nest_asyncio 
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# -----------------------------------------------------------------------------
# 1. THE FAKE WEBSITE (KEEPS BOT ALIVE)
# -----------------------------------------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "I am alive! Bot is running."

def run_http():
    # Render assigns a port automatically via the 'PORT' environment variable
    # If running locally, it defaults to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# -----------------------------------------------------------------------------
# 2. CONFIGURATION
# -----------------------------------------------------------------------------
BOT_TOKEN = "7590792220:AAG3KIXVRzOF_cnhDpk91ERfIa_l2CLFbCU"

# Apply nest_asyncio to prevent event loop errors
nest_asyncio.apply()

# Your Database
MOD_DATABASE = {
    "game1": "https://www.link1.com",
    "game2": "https://www.link2.com",
    "game3": "https://www.link3.com",
    "minecraft": "https://www.minecraftmods.com",
    "skyrim": "https://www.nexusmods.com/skyrim",
    "gta": "https://www.gta5-mods.com"
}

# -----------------------------------------------------------------------------
# 3. LOGGING SETUP
# -----------------------------------------------------------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# -----------------------------------------------------------------------------
# 4. BOT FUNCTIONS
# -----------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    instruction_message = (
        f"Hello, {user_first_name}! 👋\n\n"
        "I can help you find download links for specific game mods.\n\n"
        "**How to search:**\n"
        "Simply type the name of the game you are looking for.\n\n"
        "**Examples:**\n"
        "• game1\n"
        "• skyrim\n"
        "• gta"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=instruction_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()

    if user_text in MOD_DATABASE:
        found_link = MOD_DATABASE[user_text]
        response = f"✅ **Mod Found!**\n\nHere is the link for {user_text}:\n{found_link}"
    else:
        response = (
            f"❌ Sorry, I couldn't find a mod for '{user_text}'.\n"
            "Please check the spelling or try a different game name."
        )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# -----------------------------------------------------------------------------
# 5. MAIN EXECUTION
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    # Start the fake website in the background
    keep_alive()
    
    print("Bot is starting...")
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)
    
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    print("Bot is running!")
    
    # Run the bot
    application.run_polling()
