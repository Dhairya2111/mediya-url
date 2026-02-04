# Telegram File to URL Bot

This bot converts any image, video, or document sent to it into a public direct URL using the Catbox API.

## Setup Instructions

1.  **Get API Credentials:**
    - Go to [my.telegram.org](https://my.telegram.org) to get your `API_ID` and `API_HASH`.
    - Message [@BotFather](https://t.me/BotFather) on Telegram to get a `BOT_TOKEN`.

2.  **Environment Variables:**
    - Set the following environment variables or edit them directly in `main.py`:
      - `API_ID`
      - `API_HASH`
      - `BOT_TOKEN`

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Bot:**
    ```bash
    python main.py
    ```

## Usage
- Send any photo, video, or GIF to the bot.
- The bot will reply with a permanent `https://catbox.moe/...` link.