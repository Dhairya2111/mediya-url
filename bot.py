import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    print('------')

@bot.command(name='ping')
async def ping(ctx):
    """Responds with the bot's latency."""
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(name='echo')
async def echo(ctx, *, message: str):
    """Repeats the user's message."""
    await ctx.send(message)

if __name__ == '__main__':
    if TOKEN:
        bot.run(TOKEN)
    else:
        print('Error: DISCORD_TOKEN not found in environment variables.')