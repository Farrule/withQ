import os
import asyncio

import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.interactions import Interaction
from dotenv import load_dotenv

# get bot TOKEN from ./env file
load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")

# instance
intents = discord.Intents.default()
# intents.members = True
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


class InQButton(Button):
    def __init__(self):
        super().__init__(label="IN Q", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        await interaction.response.send_message("aaa")


class DeQButton(Button):
    def __init__(self):
        super().__init__(label="DE Q", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        await interaction.response.send_message("ddd")


class CancelButton(Button):
    def __init__(self):
        super().__init__(label="CANCEL", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        await interaction.response.send_message("aaa")


class RowView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(InQButton())
        self.add_item(DeQButton())
        self.add_item(CancelButton())


# startup process
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def w(ctx, *delete_time: int):
    """withQ command"""


    try:
        if (delete_time[0]):
            await ctx.send("test", view=RowView(), delete_after=delete_time[0]*60)
            await asyncio.sleep(delete_time[0]*60)
            await ctx.message.delete()


    except:
        await ctx.send("except")


bot.run(TOKEN)
