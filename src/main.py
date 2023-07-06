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
    def __init__(self, title: str, recruitment_num: int, in_queue_member_list: list):
        super().__init__(label="IN Q", style=discord.ButtonStyle.primary)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_list = in_queue_member_list

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        if interaction.user.mention not in self.in_queue_member_list:
            self.in_queue_member_list.append(interaction.user.mention)
            if len(self.in_queue_member_list) == self.recruitment_num:
                mentions = ""
                for in_q_member in self.in_queue_member_list:
                    mentions += in_q_member
                await interaction.response.edit_message(
                    content=f'{mentions}\n{self.title}\n上記の募集が完了しました。',
                    view=None,
                )

                return
            await interaction.response.edit_message(
                content=f'{self.title}  @{self.recruitment_num - len(self.in_queue_member_list)}'
            )
            await interaction.followup.send("この募集に参加しました。", ephemeral=True)
            print(self.in_queue_member_list)
        elif interaction.user.mention in self.in_queue_member_list:
            await interaction.response.send_message("すでにこの募集に参加しています。", ephemeral=True)
            print(self.in_queue_member_list)


class DeQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_list: list):
        super().__init__(label="DE Q", style=discord.ButtonStyle.red)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_list = in_queue_member_list

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        if interaction.user.mention in self.in_queue_member_list:
            self.in_queue_member_list.remove(interaction.user.mention)
            await interaction.response.edit_message(
                content=f'{self.title}  @{self.recruitment_num + len(self.in_queue_member_list)}'
            )
            await interaction.followup.send("この募集への参加を取り消しました。", ephemeral=True)
            print(self.in_queue_member_list)
        elif interaction.user.mention not in self.in_queue_member_list:
            await interaction.response.send_message("あなたはこの募集に参加していません。", ephemeral=True)
            print(self.in_queue_member_list)


class CancelButton(Button):
    def __init__(self):
        super().__init__(label="CANCEL", style=discord.ButtonStyle.grey)

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        await interaction.response.edit_message(content="この募集は終了しました。", view=None)


class RowView(View):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_list: list):
        super().__init__(timeout=None)
        self.add_item(InQButton(title, recruitment_num, in_queue_member_list))
        self.add_item(DeQButton(title, recruitment_num, in_queue_member_list))
        self.add_item(CancelButton())


# startup process
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def w(ctx, title: str, recruitment_num: int, *delete_time: int):
    """withQ command"""

    in_queue_member_list = []

    try:
        if len(delete_time) != 0:
            await ctx.send(f'`{title}`  @`{recruitment_num}`', view=RowView(title, recruitment_num, in_queue_member_list), delete_after=delete_time[0]*60)
            await asyncio.sleep(delete_time[0]*60)
            await ctx.message.delete()

        if len(delete_time) == 0:
            await ctx.send(f'`{title}`  @`{recruitment_num}`', view=RowView(title, recruitment_num, in_queue_member_list))


    except:
        await ctx.send("except")


bot.run(TOKEN)
