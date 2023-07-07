import os
import asyncio
import re
import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

import component.row_view as row_view
import constants.regex as regex

# get bot TOKEN from ./env file
load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")

HERE_MENTION = "@here"
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
    *args,
    # *delete_time: int,
):
    """withQ command"""

    now_datetime = datetime.datetime.now()
    now_time = str(now_datetime.hour) + str(now_datetime.minute)
    # key: 参加者ユーザーネーム value:メンションID
    in_queue_member_dict = {
        ctx.message.author.global_name: ctx.message.author.mention}
    recruiter = ctx.author

    try:
        print(args)
        for setting_parm in args:
            if re.match(regex.START_TIME, str(setting_parm)) != None:
                start_time = str(setting_parm).replace(
                    ':', '').replace('~', '')
                if int(start_time) >= int(now_time):
                    bot_message = await ctx.send(
                        f'{title}  @{recruitment_num}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                        view=row_view.RowView(
                            title, recruitment_num, in_queue_member_dict, recruiter)
                    )
                    await asyncio.sleep((int(start_time) - int(now_time))*60)
                    mentions = ""
                    for mention in in_queue_member_dict.values():
                        mentions += mention + ' '
                    await bot_message.edit(
                        content=f'{mentions}\n{title}\n上記の募集を締め切りました。',
                        view=None,
                    )
                else:
                    await ctx.reply("開始時間の入力値を確認してください。", ephemeral=True)

            else:
                await ctx.send(
                    f'{title}  @{recruitment_num}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                    view=row_view.RowView(
                        title, recruitment_num, in_queue_member_dict, recruiter)
                )

    except:
        await ctx.send("except")


bot.run(TOKEN)
