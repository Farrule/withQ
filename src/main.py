import os
import asyncio

import discord
from discord.ext import commands
from discord.ui import Button, View
from discord.interactions import Interaction
from discord.utils import get
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
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict):
        super().__init__(label="IN Q", style=discord.ButtonStyle.primary)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        print(self.in_queue_member_dict)
        # ボタン押下者が対象の募集に参加していない場合、メンションリストとユーザーリストにボタン押下者の情報を追加する
        if interaction.user.global_name not in self.in_queue_member_dict:
            self.in_queue_member_dict[interaction.user.global_name] = interaction.user.mention
            print(self.in_queue_member_dict)
            # 募集人数に達した場合、参加者リストの参加者にメンションし募集が完了した旨を伝えるメッセージを送信する
            if len(self.in_queue_member_dict) - 1 == self.recruitment_num:
                mentions = ""
                for mention in self.in_queue_member_dict.values():
                    mentions += mention
                await interaction.response.edit_message(
                    content=f'{mentions}\n{self.title}\n上記の募集が完了しました。',
                    view=None,
                )
                return
            # 募集人数に達していない場合、募集用メッセージを編集し残りの募集人数を変更する
            if len(self.in_queue_member_dict) <= self.recruitment_num:
                users = ""
                for user in self.in_queue_member_dict:
                    if user != next(iter(self.in_queue_member_dict)):
                        users = user + ',' + users
                await interaction.response.edit_message(
                    content=f'{self.title}  @{self.recruitment_num - len(self.in_queue_member_dict) + 1}\n募集者: {next(iter(self.in_queue_member_dict))}\n参加者: {users}'
                )
                await interaction.followup.send("この募集に参加しました。", ephemeral=True)
                print(self.in_queue_member_dict)
        # ボタン押下者が対象の募集にすでに参加している場合、その旨を伝えるメッセージを送信する
        elif interaction.user.global_name in self.in_queue_member_dict:
            await interaction.response.send_message("すでにこの募集に参加しています。", ephemeral=True)
            print(self.in_queue_member_dict)


class DeQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict):
        super().__init__(label="DE Q", style=discord.ButtonStyle.red)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        print(self.in_queue_member_dict)
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message("募集主はDE Qできません。", ephemeral=True)
            return
        if interaction.user.global_name in self.in_queue_member_dict:
            self.in_queue_member_dict.pop(interaction.user.global_name)
            users = ""
            for user in self.in_queue_member_dict:
                if user != next(iter(self.in_queue_member_dict)):
                    users = user + ',' + users
            await interaction.response.edit_message(
                content=f'{self.title}  @{self.recruitment_num - len(self.in_queue_member_dict) + 1}\n募集者: {next(iter(self.in_queue_member_dict))}\n参加者: {users}'
            )
            await interaction.followup.send("この募集への参加を取り消しました。", ephemeral=True)
            print(self.in_queue_member_dict)
        elif interaction.user.global_name not in self.in_queue_member_dict.keys():
            await interaction.response.send_message("あなたはこの募集に参加していません。", ephemeral=True)
            print(self.in_queue_member_dict)


class CancelButton(Button):
    def __init__(self, in_queue_member_dict: dict):
        super().__init__(label="CANCEL", style=discord.ButtonStyle.grey)
        self.in_queue_member_dict = in_queue_member_dict

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            await interaction.response.edit_message(content="この募集は終了しました。", view=None)
            return
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を取り消すことができるのは募集主のみです。", ephemeral=True)
            return


class RowView(View):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict):
        super().__init__(timeout=None)
        self.add_item(InQButton(title, recruitment_num, in_queue_member_dict))
        self.add_item(DeQButton(title, recruitment_num, in_queue_member_dict))
        self.add_item(CancelButton(in_queue_member_dict))


# startup process
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def w(ctx, title: str, recruitment_num: int, *delete_time: int):
    """withQ command"""

    # key: 参加者ユーザーネーム value:メンションID
    in_queue_member_dict = {ctx.message.author.global_name: ctx.message.author.mention}

    try:
        if len(delete_time) != 0:
            await ctx.send(
                f'`{title}`  @`{recruitment_num}`\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=RowView(title, recruitment_num, in_queue_member_dict),
                delete_after=delete_time[0]*60
            )
            await asyncio.sleep(delete_time[0]*60)
            await ctx.message.delete()
        if len(delete_time) == 0:
            await ctx.send(
                f'`{title}`  @`{recruitment_num}`\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=RowView(title, recruitment_num, in_queue_member_dict)
            )


    except:
        await ctx.send("except")


bot.run(TOKEN)
