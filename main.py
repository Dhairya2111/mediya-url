import discord
import yt_dlp
import asyncio
from discord.ext import commands

# Bot configuration
TOKEN = 'YOUR_BOT_TOKEN_HERE'
INTENTS = discord.Intents.default()
INTENTS.message_content = True

bot = commands.Bot(command_prefix='/', intents=INTENTS)

# YDL options for audio extraction
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command(name='play')
async def play(ctx, *, search: str):
    """Plays a song from YouTube based on search query."""
    if not ctx.author.voice:
        return await ctx.send("You must be in a voice channel to use this command!")

    channel = ctx.author.voice.channel
    
    # Connect to voice channel
    if ctx.voice_client is None:
        await channel.connect()
    else:
        await ctx.voice_client.move_to(channel)

    async with ctx.typing():
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
                url = info['url']
                title = info['title']
            except Exception as e:
                return await ctx.send(f"An error occurred: {str(e)}")

        # Stop current audio if playing
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = await discord.FFmpegOpusAudio.from_probe(url, **FFMPEG_OPTIONS)
        ctx.voice_client.play(source)
        
    await ctx.send(f'Now playing: **{title}**')

@bot.command(name='stop')
async def stop(ctx):
    """Stops the music and leaves the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from voice channel.")
    else:
        await ctx.send("I am not connected to a voice channel.")

if __name__ == "__main__":
    bot.run(TOKEN)