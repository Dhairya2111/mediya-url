import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

async def main():
    async with bot:
        await bot.load_extension("music_cog")
        await bot.start("YOUR_BOT_TOKEN")

if __name__ == "__main__":
    asyncio.run(main())