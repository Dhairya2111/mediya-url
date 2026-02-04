import os, asyncio, threading, requests
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import MemorySession

app = Flask(__name__)

@app.route('/')
def home(): 
    return "Media-to-URL Bot is Running!", 200

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Use MemorySession to prevent 'sqlite3.OperationalError: database is locked'
# This is ideal for stateless deployments like Render/Heroku
bot = TelegramClient(MemorySession(), API_ID, API_HASH)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("<b>Hi! Send me any Image, Video, or Document, and I will give you a Catbox link.</b>", parse_mode='html')

@bot.on(events.NewMessage)
async def media_handler(event):
    # Ignore commands and messages without media
    if event.media and not (event.text and event.text.startswith('/')):
        msg = await event.reply("<code>⏳ Processing Media...</code>", parse_mode='html')
        file_path = await event.download_media()
        
        try:
            # Uploading to Catbox as per README instructions
            with open(file_path, 'rb') as f:
                files = {'fileToUpload': f}
                data = {'reqtype': 'fileupload'}
                response = requests.post("https://catbox.moe/user/api.php", data=data, files=files)
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            if response.status_code == 200:
                url = response.text.strip()
                await msg.edit(f"<b>✅ Link Generated:</b>\n<code>{url}</code>", parse_mode='html', link_preview=False)
            else:
                await msg.edit(f"❌ <b>Upload Failed!</b> (Status: {response.status_code})")
        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            await msg.edit(f"❌ <b>Error:</b> {str(e)}")

def run_bot():
    # Create a new event loop for the bot thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start the bot and run until disconnected
    bot.start(bot_token=BOT_TOKEN)
    print("Bot started...")
    bot.run_until_disconnected()

# Start the bot in a background thread to prevent blocking the Flask/WSGI server
# daemon=True ensures the thread closes when the main process exits
threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)