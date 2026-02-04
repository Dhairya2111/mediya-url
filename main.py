import os, asyncio, threading, requests
from flask import Flask
from telethon import TelegramClient, events

app = Flask(__name__)

@app.route('/')
def home(): 
    return "Media-to-URL Bot is Running!", 200

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Initialize client without starting it immediately at module level
bot = TelegramClient('bot', API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("<b>Hi! Send me any Image or Video, and I will give you a Telegraph link.</b>", parse_mode='html')

@bot.on(events.NewMessage)
async def media_handler(event):
    # Ignore commands and messages without media
    if event.media and not (event.text and event.text.startswith('/')):
        msg = await event.reply("<code>🔄 Processing Media...</code>", parse_mode='html')
        file_path = await event.download_media()
        
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    "https://telegra.ph/upload", 
                    files={'file': ('file', f, 'image/jpg')}
                ).json()
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            if isinstance(response, list) and len(response) > 0 and 'src' in response[0]:
                url = f"https://telegra.ph{response[0]['src']}"
                await msg.edit(f"<b>✅ Link Generated:</b>\n<code>{url}</code>", parse_mode='html', link_preview=False)
            else:
                await msg.edit("❌ <b>Upload Failed!</b>")
        except Exception as e:
            await msg.edit(f"❌ <b>Error:</b> {str(e)}")

def run_bot():
    # Create a new event loop for the bot thread to avoid conflicts with WSGI
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot.start(bot_token=BOT_TOKEN)
    bot.run_until_disconnected()

# Start the bot in a background thread so it doesn't block the WSGI server
# This prevents the 'run_until_complete' error during module import
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    # This block is used for local development
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)