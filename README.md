# Telegram Start Bot

A simple boilerplate for a Telegram bot using the `python-telegram-bot` library.

## Setup Instructions

1. **Get a Token**: Message [@BotFather](https://t.me/botfather) on Telegram to create a bot and get your API token.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Environment Variable**:
   - Linux/macOS: `export TELEGRAM_BOT_TOKEN='your_token_here'`
   - Windows: `set TELEGRAM_BOT_TOKEN=your_token_here`
   - *Alternatively, paste the token directly into `main.py` (not recommended for production).*
4. **Run the Bot**:
   ```bash
   python main.py
   ```

## Commands
- `/start`: Greets the user.
- `/help`: Lists available commands.