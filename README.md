# Discord Music Bot

A simple Discord bot to play music from YouTube.

## Prerequisites
1. Install [FFmpeg](https://ffmpeg.org/download.html) on your system and ensure it's in your PATH.
2. Create a Discord Bot on the [Developer Portal](https://discord.com/developers/applications).
3. Enable `Message Content Intent` in the Bot settings.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Open `main.py` and replace `YOUR_BOT_TOKEN_HERE` with your actual bot token.
3. Run the bot:
   ```bash
   python main.py
   ```

## Usage
- `/play <song name or url>`: Joins your voice channel and plays the song.
- `/stop`: Stops the music and leaves the channel.