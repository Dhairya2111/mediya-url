import os, asyncio, threading, requests
from flask import Flask
from telethon import TelegramClient, events
from telethon.sessions import StringSession

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running perfectly!", 200

API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION = os.getenv("SESSION_STRING", "")

client = TelegramClient(StringSession(SESSION), API_ID, API_HASH)

@client.on(events.NewMessage(outgoing=True))
async def media_handler(event):
    if event.media:
        await event.edit("<code>🔄 Uploading to Telegraph...</code>", parse_mode='html')
        file_path = await event.download_media()
        try:
            with open(file_path, 'rb') as f:
                response = requests.post(
                    "https://telegra.ph/upload", 
                    files={'file': ('file', f, 'image/jpg')}
                ).json()
            if os.path.exists(file_path):
                os.remove(file_path)
            if isinstance(response, list) and 'src' in response[0]:
                url = f"https://telegra.ph{response[0]['src']}"
                await event.edit(f"<b>✅ Link:</b> <code>{url}</code>", parse_mode='html', link_preview=False)
            else:
                await event.edit("❌ <b>Upload Failed!</b>")
        except Exception as e:
            await event.edit(f"❌ <b>Error:</b> {str(e)}")

def run_flask():
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot starting...")
    client.start()
    client.run_until_disconnected()