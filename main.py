import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Replace with your actual Bot Token from @BotFather
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a greeting message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Namaste {user.mention_html()}! 🙏\n\nMain aapka updated bot hoon. Main kaam karne ke liye taiyar hoon."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a help message."""
    await update.message.reply_text("Aap /start dabayein bot shuru karne ke liye.")

if __name__ == '__main__':
    # Create the Application
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    print("Bot is running...")
    application.run_polling()