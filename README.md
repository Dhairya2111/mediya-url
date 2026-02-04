# Telegram Music Bot

A powerful Telegram Music Bot that plays high-quality audio in group voice chats.

## Setup Instructions

1. **Get API Credentials:**
   - Get `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org).
   - Get `BOT_TOKEN` from [@BotFather](https://t.me/BotFather).

2. **Generate Session String:**
   - You need a Pyrogram Session String for the user account that will join the voice chat. Use a session generator script or library.

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure:**
   - Open `main.py` and replace the placeholders with your actual credentials.

5. **Run the Bot:**
   ```bash
   python main.py
   ```

## Commands
- `/play <song name>`: Search and play music.
- `/stop`: Stop the music and leave the chat.
- `/start`: Check if the bot is alive.