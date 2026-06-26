import logging
from discord.ext import commands
import discord
from utils.initializer import restore_sessions

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.CustomActivity(name="In Q with your friends!"))
        logging.info(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")

        # コマンドツリーの同期
        try:
            await self.bot.tree.sync()
            logging.info("Command tree update success!")
        except Exception as e:
            logging.info("Command tree update failure!")
            logging.error(e)

        # セッションの復元
        await restore_sessions(self.bot)
        logging.info("------")

async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))