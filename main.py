import asyncio
import datetime
import os
import random
import re
from os.path import dirname, join

import discord
from discord.ext import commands
from dotenv import load_dotenv

import withQ.libs.components.deadline_time as dt
import withQ.libs.constants.const as c
import withQ.libs.constants.embed as embed
import withQ.libs.constants.regex as regex
import withQ.libs.row_view as row_view
from withQ.config.keep_alive import keep_alive

# .envファイルを取得する
load_dotenv(verbose=True)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
env_file_path = os.path.join(parent_dir, ".env")
load_dotenv(env_file_path)


# .envファイルのEXECUTION_ENVパラメータで実行環境とbotの切り替えを行う
if os.getenv("EXECUTION_ENV") == "DEBUG":
    TOKEN = os.getenv("DEVELOPMENT_TOKEN")
    print(f'USE DEVELOPMENT TOKEN:{TOKEN}')
    import withQ.tests.development_const as env_c

elif os.environ.get("EXECUTION_ENV") == "PRODUCTION":
    TOKEN = os.environ.get("PRODUCTION_TOKEN")
    print(f'USE PRODUCTION TOKEN:{TOKEN}')
    import withQ.config.production_const as env_c

else:
    print('Can`t Start This Service')

# intents
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


# bot起動時にステータスメッセージを変更してbotの情報を出力する
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name="In Q with your friends!"))
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


# withQコマンドが送信された時にembedを送信する
@bot.command()
async def withQ(ctx):
    """withQ help command"""

    await ctx.send(embed=embed.embed)


@bot.command()
async def w(
    ctx,
    title: str,
    recruitment_num: int,
    *args,
):
    """withQ command"""

    now_datetime = datetime.datetime.now() + datetime.timedelta(hours=9)
    # key: 参加者ユーザーネーム value:メンションID
    in_queue_member_dict = {
        ctx.message.author.global_name: ctx.message.author.mention
    }
    recruiter = ctx.author
    mention_target = ""
    is_feedback_on_recruitment = True
    deadline_time = ""
    total_seconds = env_c.AUTO_DEADLINE
    is_deadline = False

    try:
        # 募集人数が1人以上でない場合、returnする
        if recruitment_num <= 0:
            return

        for setting_param in args:
            # setting_param: @here形式の場合に処理を行う
            if re.match(regex.MENTION_IS_HERE, str(setting_param)) != None and mention_target == "":
                mention_target = c.HERE_MENTION
            # setting_param: @everyone形式の場合に処理を行う
            if re.match(regex.MENTION_IS_EVERYONE, str(setting_param)) != None and mention_target == "":
                mention_target = c.EVE_MENTION
            # setting_param: is_feedback_on_recruitment形式の場合に処理を行う
            if re.match(regex.FEEDBACK_ON_RECRUITMENT, str(setting_param)) != None:
                is_feedback_on_recruitment = False
            # setting_param: 開始時間の形式の場合に自動的に締め切り処理を行う
            if re.match(regex.DATETIME_TYPE, str(setting_param)) != None:
                total_seconds, deadline_time, is_deadline = dt.deadline_time(
                    deadline_time, setting_param, now_datetime, is_deadline)
            # setting_param: 開始時間が設定されていない場合、締め切り時間を設定する
            if re.match(regex.DATETIME_TYPE, str(setting_param)) == None:
                total_seconds = env_c.AUTO_DEADLINE

        print(f'締め切り時間:{total_seconds} sec')

        # 募集メッセージを作成、送信する
        bot_message = await ctx.send(
            f'{mention_target}\n{title}  @{recruitment_num} {deadline_time if deadline_time != None else ""}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
            view=row_view.RowView(
                title,
                recruitment_num,
                in_queue_member_dict,
                recruiter,
                mention_target,
                is_feedback_on_recruitment,
                deadline_time,
                is_deadline,
            )
        )

        if total_seconds > 0:
            await asyncio.sleep(total_seconds)
            if "False" != in_queue_member_dict[next(iter(reversed(in_queue_member_dict)))]:
                if len(in_queue_member_dict) <= 1:
                    await bot_message.edit(
                        content=f'{title}\n上記の募集は成立しませんでした。',
                        view=None,
                    )
                    print('---no member recruitment time out---')
                    return
                if len(in_queue_member_dict) >= 1:
                    mentions = ""
                    for mention in in_queue_member_dict.values():
                        mentions += mention + ' '
                    await bot_message.edit(
                        content=f'{mentions}\n{title}  {deadline_time}\n{c.DEADLINE_TEXT}になりましたので上記の募集を締め切りました。',
                        view=None,
                    )
                    print('---anyone member recruitment time out---')
                    return

    except:
        await ctx.send("募集を開始できませんでした。")
        return


@bot.command()
async def playW(
    ctx,
    *args,
):
    """Runlet command"""

    try:
        print("playW command")
        candidate = []

        # コマンドで受け取った候補を配列に格納する
        for temp in args:
            candidate.append(temp)

        print(candidate)

        # 候補配列からランダムに1つ選び、メッセージを送信する
        await ctx.send(
            f'{candidate[random.randint(0, len(candidate))]}'
        )

    except:
        await ctx.send("error occurred")
        return

keep_alive()
bot.run(TOKEN)
