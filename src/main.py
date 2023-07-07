import os
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

import component.row_view as row_view

# get bot TOKEN from ./env file
load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")

HERE_MENTION ="@here"
EVE_MENTION = "@everyone"

# instance
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


# startup process
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.change_presence(activity=discord.Game(name="In Q with your friends!"))


@bot.command()
async def w(
    ctx,
    title: str,
    recruitment_num: int,
    *delete_time: int,
    ):
    """withQ command"""

    # key: 参加者ユーザーネーム value:メンションID
    in_queue_member_dict = {ctx.message.author.global_name: ctx.message.author.mention}
    recruiter = ctx.author


    try:
        # 時間制限パラメータが設定されている場合に実行する
        if len(delete_time) > 0:
            await ctx.send(
                f'{title}  @{recruitment_num}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=row_view.RowView(title, recruitment_num, in_queue_member_dict, recruiter),
                delete_after=delete_time[0]*60
            )
            await asyncio.sleep(delete_time[0]*60)
            await ctx.message.delete()

        # 時間制限パラメータが設定されていない場合に実行する
        if len(delete_time) == 0:
            await ctx.send(
                f'{title}  @{recruitment_num}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=row_view.RowView(title, recruitment_num, in_queue_member_dict, recruiter)
            )

        # TODO end_time: 締め切り時間パラメータが設定されている場合に実行する


    except:
        await ctx.send("except")


bot.run(TOKEN)
