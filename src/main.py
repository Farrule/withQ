import logging
import asyncio
import discord
from discord.ext import commands
from config.settings import env_c, TOKEN

# ロギング設定
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

if env_c.DEBUG_MODE:
    logging.info("------\nService Status: DEBUG")
else:
    logging.info("------\nService Status: PRODUCTION")

# Bot初期化 (discord.Client から commands.Bot に変更)
intents = discord.Intents.all()
intents.message_content = True
allowed = discord.AllowedMentions.all()
bot = commands.Bot(command_prefix="!", intents=intents, allowed_mentions=allowed)

async def load_extensions():
    """Cogsの読み込み"""
    await bot.load_extension("cogs.events")
    await bot.load_extension("cogs.app_commands")

async def main():
    if not TOKEN:
        logging.error("==================================================")
        logging.error("❌ CRITICAL ERROR: DiscordのTOKENが設定されていません!")
        logging.error("==================================================")
        return

    async with bot:
        await load_extensions()
        await bot.start(TOKEN, reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())