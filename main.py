import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Configure Logging
logging.basicConfig(level=logging.INFO)

# --- CONFIGURATION ---
# Get these from https://my.telegram.org
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")

# This bot uses a public file hosting service (Telegraph for images, or local logic)
# For videos/files, we will simulate a direct link via a simple web server or use a public uploader
# In this version, we use 'catbox.moe' API for generating permanent URLs for both images and videos
import requests

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload"}
    files = {"fileToUpload": open(file_path, "rb")}
    response = requests.post(url, data=data, files=files)
    return response.text

app = Client("url_gen_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 **Welcome to File to URL Bot!**\n\n"
        "Send me any Image or Video, and I will provide you a direct download link."
    )

@app.on_message(filters.photo | filters.video | filters.document | filters.animation)
async def handle_files(client, message):
    msg = await message.reply_text("⏳ **Processing... Please wait.**", quote=True)
    
    try:
        # Download file from Telegram
        file_path = await message.download()
        
        await msg.edit_text("🚀 **Uploading to Server...**")
        
        # Upload to Catbox
        file_url = upload_to_catbox(file_path)
        
        # Clean up local file
        if os.path.exists(file_path):
            os.remove(file_path)

        if file_url.startswith("http"):
            await msg.edit_text(
                f"✅ **File Uploaded Successfully!**\n\n🔗 **URL:** `{file_url}`",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🌐 Open Link", url=file_url)]
                ])
            )
        else:
            await msg.edit_text(f"❌ **Upload Failed:** {file_url}")
            
    except Exception as e:
        await msg.edit_text(f"❌ **Error:** {str(e)}")

if __name__ == "__main__":
    print("Bot is running...")
    app.run()