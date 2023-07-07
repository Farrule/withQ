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
):
    """withQ command"""

    now_datetime = datetime.datetime.now()
    now_time = str(now_datetime.hour) + str(now_datetime.minute)
    # key: 参加者ユーザーネーム value:メンションID
    in_queue_member_dict = {
        ctx.message.author.global_name: ctx.message.author.mention}
    recruiter = ctx.author
    mention_target = ""

    try:
        print(args)
        for setting_parm in args:
            # setting_param: @here形式の場合に処理を行う
            print(setting_parm)
            print(re.match(regex.MENTION_IS_HERE, str(setting_parm)))
            if re.match(regex.MENTION_IS_HERE, str(setting_parm)) != None and mention_target == "":
                mention_target = "@here"
            # setting_param: @everyone形式の場合に処理を行う
            if re.match(regex.MENTION_IS_EVERYONE, str(setting_parm)) != None and mention_target == "":
                mention_target = "@everyone"
            # 募集メッセージを作成、送信する
            bot_message = await ctx.send(
                f'{mention_target}\n{title}  @{recruitment_num}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=row_view.RowView(
                    title, recruitment_num, in_queue_member_dict, recruiter, mention_target
                )
            )
            # setting_parm: 開始時間の形式の場合に自動的に締め切り処理を行う
            if re.match(regex.START_TIME, str(setting_parm)) != None:
                start_time = str(setting_parm).replace(
                    ':', '').replace('~', '')
                if int(start_time) >= int(now_time):
                    await asyncio.sleep((int(start_time) - int(now_time))*60)
                    mentions = ""
                    for mention in in_queue_member_dict.values():
                        mentions += mention + ' '
                    await bot_message.edit(
                        content=f'{mentions}\n{title}\n上記の募集を締め切りました。',
                        view=None,
                    )

    except:
        await ctx.send("error occurred")


bot.run(TOKEN)
