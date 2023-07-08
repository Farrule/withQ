import asyncio
import datetime
import os
import re
from os.path import dirname, join

import discord
from discord.ext import commands
from dotenv import load_dotenv

import components.row_view as row_view
import constants.regex as regex

# get bot TOKEN from ./env file
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
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
    # key: 参加者ユーザーネーム value:メンションID
    in_queue_member_dict = {
        ctx.message.author.global_name: ctx.message.author.mention}
    recruiter = ctx.author
    mention_target = ""
    is_feedback_on_recruitment = True
    promised_time = ""
    total_seconds = 0

    try:
        print(args)
        for setting_param in args:
            # setting_param: @here形式の場合に処理を行う
            if re.match(regex.MENTION_IS_HERE, str(setting_param)) != None and mention_target == "":
                mention_target = "@here"
            # setting_param: @everyone形式の場合に処理を行う
            if re.match(regex.MENTION_IS_EVERYONE, str(setting_param)) != None and mention_target == "":
                mention_target = "@everyone"
            # setting_param: is_feedback_on_recruitment形式の場合に処理を行う
            if re.match(regex.FEEDBACK_ON_RECRUITMENT, str(setting_param)) != None:
                is_feedback_on_recruitment = False
            # setting_param: 開始時間の形式の場合に自動的に締め切り処理を行う
            if promised_time != None:
                if re.match(regex.START_TIME, str(setting_param)) != None:
                    time_in_seconds = datetime.datetime.fromtimestamp(
                        setting_param.replace(':', ''))
                    if time_in_seconds >= now_datetime:
                        promised_time = "開始時刻: " + setting_param
                        time_delta = time_in_seconds - now_datetime
                        total_seconds = time_delta.total_seconds()
                if re.match(regex.START_DATETIME, str(setting_param)) != None:
                    time_in_datetime = datetime.datetime.fromtimestamp(
                        setting_param.replace('/'), ''.replace(':', ''))
                    if time_in_datetime >= now_datetime:
                        promised_time = "開始時刻: " + setting_param
                        time_delta = time_in_datetime - now_datetime
                        total_seconds = time_delta.total_seconds()
                if re.match(regex.START_YEARDATETIME, str(setting_param)) != None:
                    time_in_datetime = datetime.datetime.fromtimestamp(
                        setting_param.replace('/'), ''.replace(':', ''))
                    if time_in_datetime >= now_datetime:
                        promised_time = "開始時刻: " + setting_param
                        time_delta = time_in_datetime - now_datetime
                        total_seconds = time_delta.total_seconds()
        # 募集メッセージを作成、送信する
        bot_message = await ctx.send(
            f'{mention_target}\n\
            {title}  @{recruitment_num} {promised_time if promised_time != None else ""}\n\
            募集者: {next(iter(in_queue_member_dict))}\n\
            参加者:',
            view=row_view.RowView(
                title,
                recruitment_num,
                in_queue_member_dict,
                recruiter,
                mention_target,
                is_feedback_on_recruitment,
                promised_time
            )
        )
        if total_seconds >= 0:
            await asyncio.sleep(total_seconds)
            mentions = ""
            for mention in in_queue_member_dict.values():
                mentions += mention + ' '
            await bot_message.edit(
                content=f'{mentions}\n\
                        {title}\n\
                        開始時間になりましたので上記の募集を締め切りました。',
                view=None,
            )
            return

    except:
        await ctx.send("error occurred")
        return


bot.run(TOKEN)
