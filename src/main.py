import asyncio
import datetime
import os
import random
import re
from os.path import dirname, join

import discord
from discord.ext import commands
from dotenv import load_dotenv

import libs.components.deadline_time as dt
import libs.constants.const as c
import libs.constants.regex as regex
import libs.row_view as row_view

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
    import tests.development_const as env_c

elif os.environ.get("EXECUTION_ENV") == "PRODUCTION":
    TOKEN = os.environ.get("PRODUCTION_TOKEN")
    print(f'USE PRODUCTION TOKEN:{TOKEN}')
    import config.production_const as env_c

else:
    print('Can`t Start This Service')

# intents
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='/', intents=intents)


# startup process
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="In Q with your friends!"))
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
async def withQ(ctx):
    """withQ help command"""

    embed = discord.Embed(
        title="withQの使い方",
        description='withQ は、Discord でゲームをする複数の友人に対して一緒にゲームをプレイする機会を提供するボットです。\n'
        'withQ の使用方法は、以下のとおりです。\n'
        '\n'
        '**コマンドの入力方法**\n'
        '```/w [タイトル] [募集人数] [締め切り時間] [メンション] [参加者通知設定]```\n'
        '\n'
        '**各値について**\n'
        '\n'
        '※必須値は必ず上記のコマンド順で入力してください。オプション値は順不問となり、設定されていなくても問題ありません。\n'
        '※[締め切り時間]の値が設定されていない場合、6時間後に自動で募集が取り消されます。\n'
        '\n'
        '**[タイトル]**・・・必須値。募集したい内容やタイトルを入力します\n'
        '\n'
        '**[募集人数]**・・・必須値。募集したい人数を入力します。募集人数に達したときに募集を終了して参加者をメンションします\n'
        '\n'
        '**[締め切り時間]**・・・オプション値。募集に締め切り時間を設定したい場合に利用できます。値が設定されていない場合、6時間後に募集が取り消されます\n'
        '\n'
        '有効な値は以下の通りです。\n'
        'コマンドの値・・・機能\n'
        'hh:mm・・・入力された時間に募集を締め切ります。\n'
        'mm/dd/hh:mm・・・入力された日付と時間に募集を締め切ります。  \n'
        'yyyy/mm/dd/hh:mm・・・入力された年月日と時間に募集を締め切ります。\n'
        '\n'
        '**[メンション]**・・・オプション値。botが送信する募集メッセージに @everyone または @here のメンションを追加したい場合に利用できます\n'
        '\n'
        '有効な値は以下の通りです。\n'
        'コマンドの値・・・機能\n'
        'e・・・募集メッセージに @everyone を付与します。\n'
        'h・・・募集メッセージに @here を付与します。\n'
        '\n'
        '**[参加者通知設定]**・・・オプション。参加者通知設定コマンドがある場合に募集者に送信される参加通知DMと参加取り消し通知DMを送信しないようにできます\n'
        '\n'
        '有効な値は以下の通りです。\n'
        'コマンドの値・・・機能\n'
        'n・・・参加通知DMと参加取り消しDMを無効にします。\n'
        '\n'
        '**募集メッセージの各ボタンについて**\n'
        '\n'
        'コマンドによって withQ が送信する募集メッセージには IN Qボタン、DE Qボタン、〆ボタン、CANCELボタンの4種類のボタンが存在します。\n'
        '\n'
        '各ボタンの機能については以下の通りです。\n'
        'ボタン名・・・機能\n'
        'IN Q・・・押下することで募集に参加することができます。\n'
        'DE Q・・・すでに対象の募集に参加している場合、押下することで募集を取り消すことができます。\n'
        '〆・・・募集者のみが押下することができます。押下時点で募集を締め切り、参加者をメンションします。\n'
        'CANCEL・・・募集者のみが押下することができます。押下することで募集を終了することができます。\n'
    )

    await ctx.send(embed=embed)


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

bot.run(TOKEN)
