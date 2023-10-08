import asyncio
import datetime
import os
import re

import discord
from discord.ext import commands

import components.constants.const as c
import components.constants.regex as regex
import components.deadline_time as dt
import components.row_view as row_view
import components.create_embed as create_embed
from keep_alive import keep_alive

TOKEN = os.environ['DISCORD_TOKEN']
# instance
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


# startup process
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    await bot.change_presence(activity=discord.Game(
        name="In Q with your friends!"))

@bot.command()
async def withQ(ctx):
    """withQ help command"""

    embed=discord.Embed(description=c.EMBED_TEXT)
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
    total_seconds = 0
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
            if re.match(regex.DATETIME_TYPE, str(setting_param)) == None:
                total_seconds = c.AUTO_DEADLINE
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
                mentions = ""
                for mention in in_queue_member_dict.values():
                    mentions += mention + ' '
                await bot_message.edit(
                    content=f'{mentions}\n{title}  {deadline_time}\n{c.DEADLINE_TEXT}になりましたので上記の募集を締め切りました。',
                    view=None,
                )
                return

    except:
        await ctx.send("error occurred")
        return


keep_alive()
bot.run(TOKEN)
