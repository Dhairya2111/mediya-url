import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
from yt_dlp import YoutubeDL

# --- CONFIGURATION ---
API_ID = 1234567  # Get from my.telegram.org
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"
SESSION_STRING = "your_pyrogram_session" # String session of a user account to join VCs

# Initialize Clients
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_app = Client("UserAssistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
call_py = PyTgCalls(user_app)

YDL_OPTIONS = {"format": "bestaudio/best", "quiet": True, "noplaylist": True}

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("👋 Hello! I am a high-quality Music Bot.\n\nCommands:\n/play [song name] - Play music\n/stop - Stop music\n/skip - Skip current track")

@bot.on_message(filters.command("play") & filters.group)
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a song name!")
    
    query = " ".join(message.command[1:])
    m = await message.reply_text("🔎 Searching...")

    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
            title = info['title']

        await call_py.join_group_call(
            message.chat.id,
            AudioPiped(url)
        )
        await m.edit(f"🎶 **Started Playing:** {title}")
    except Exception as e:
        await m.edit(f"❌ Error: {str(e)}")

@bot.on_message(filters.command("stop") & filters.group)
async def stop(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("⏹ Stopped and left the voice chat.")
    except:
        await message.reply_text("❌ Not currently playing anything.")

async def main():
    await bot.start()
    await user_app.start()
    await call_py.start()
    print("Bot is running...")
    await idle()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())