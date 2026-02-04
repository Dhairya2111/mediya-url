import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    user = update.effective_user
    message = (
        f"Hello {user.first_name}! 👋\n\n"
        "I am a Python-based Telegram bot.\n"
        "You can use /help to see what I can do."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command."""
    help_text = (
        "Available Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

if __name__ == '__main__':
    # Replace 'YOUR_TOKEN_HERE' with your actual BotFather token or use environment variables
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_TOKEN_HERE")
    
    if TOKEN == "YOUR_TOKEN_HERE":
        print("Error: Please set your TELEGRAM_BOT_TOKEN in environment variables or main.py")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        
        start_handler = CommandHandler('start', start)
        help_handler = CommandHandler('help', help_command)
        
        application.add_handler(start_handler)
        application.add_handler(help_handler)
        
        print("Bot is running...")
        application.run_polling()