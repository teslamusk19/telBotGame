import logging
import os
import asyncio # <--- Added this for the delays
from threading import Thread
from flask import Flask
import nest_asyncio 
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# -----------------------------------------------------------------------------
# 1. THE FAKE WEBSITE (KEEPS BOT ALIVE)
# -----------------------------------------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "System Online. Hacking in progress..."

def run_http():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_http)
    t.start()

# -----------------------------------------------------------------------------
# 2. CONFIGURATION
# -----------------------------------------------------------------------------
BOT_TOKEN = "7590792220:AAG3KIXVRzOF_cnhDpk91ERfIa_l2CLFbCU"

nest_asyncio.apply()

# The Rick Roll Database
MOD_DATABASE = {
    "forza": "https://bit.ly/3XzGQEq",
    "freefire": "https://bit.ly/3XzGQEq",
    "rdr": "https://bit.ly/3XzGQEq",
    "minecraft": "https://bit.ly/3XzGQEq",
    "skyrim": "https://bit.ly/3XzGQEq",
    "gta": "https://bit.ly/3XzGQEq"
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
    
    # A more "terminal-like" welcome message
    instruction_message = (
        f"💻 **TERMINAL V2.0 ONLINE**\n"
        f"User: {user_first_name}\n"
        f"Status: Connected to Dark Node\n\n"
        "Enter target keyword to initiate extraction protocol.\n\n"
        "**Available Targets:**\n"
        "`> forza`\n"
        "`> freefire`\n"
        "`> gta`"
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=instruction_message, 
        parse_mode=constants.ParseMode.MARKDOWN
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower().strip()
    chat_id = update.effective_chat.id

    # 1. Send the initial "Loading" message
    status_msg = await context.bot.send_message(
        chat_id=chat_id, 
        text="`[ ] Initializing HackTool...`",
        parse_mode=constants.ParseMode.MARKDOWN
    )

    # 2. The Fake Hacking Sequence (The "Unhinged" part)
    # We edit the SAME message repeatedly to create animation
    steps = [
        "`[█] Bypassing Mainframe Firewall...`",
        "`[██] Accessing Dark Web Node (192.168.X.X)...`",
        f"`[███] Searching database for '{user_text}'...`",
        "`[████] Encrypted packet found. Decrypting (AES-256)...`",
        "`[█████] Extraction complete. Generating link...`"
    ]

    for step in steps:
        await asyncio.sleep(1.0) # Wait 1 second between steps
        try:
            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=status_msg.message_id,
                text=step,
                parse_mode=constants.ParseMode.MARKDOWN
            )
        except Exception:
            pass # Ignore errors if user deletes chat mid-hack

    # 3. The Final Reveal
    await asyncio.sleep(0.5)
    
    if user_text in MOD_DATABASE:
        found_link = MOD_DATABASE[user_text]
        final_response = (
            f"💀 **SYSTEM BREACH SUCCESSFUL** 💀\n\n"
            f"**Target:** {user_text.upper()}\n"
            f"**Source:** [REDACTED]\n"
            f"**File Size:** 42.0 GB\n\n"
            f"⬇️ **SECURE DOWNLOAD LINK:**\n{found_link}"
        )
    else:
        final_response = (
            f"❌ **SYSTEM FAILURE**\n\n"
            f"Target '{user_text}' not found in the matrix.\n"
            "Try a different keyword."
        )

    # Replace the loading text with the final result
    await context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=status_msg.message_id,
        text=final_response,
        parse_mode=constants.ParseMode.MARKDOWN
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="`ERR: Unknown Command.`", parse_mode=constants.ParseMode.MARKDOWN)

# -----------------------------------------------------------------------------
# 5. MAIN EXECUTION
# -----------------------------------------------------------------------------
if __name__ == '__main__':
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
    
    application.run_polling()
