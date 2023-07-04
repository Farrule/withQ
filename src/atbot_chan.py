import asyncio
import os
import re
import sys

import discord
from discord.ext import commands

# TODO:os.environ['DISCORD_BOT_TOKEN']
TOKEN = os.environ["DISCORD_BOT_TOKEN"]
# TODO:コマンド変更時
bot = commands.Bot(command_prefix="!")
Emcompre = "!"
# TODO:バージョン変更時
botver = "1.0.2"

flag = True
b_count = 0
o_flag = 0
m_count = 0
# 募集時メンバーリスト
MEMBER_LIST = []
# MEMBER_LIST結果出力用
MEMBER_DIS = []
# UNICODE
ONE = "\N{Large Red Circle}"
TWO = "\N{Large Blue Circle}"
THREE = "\N{Large Yellow Circle}"
FOUR = "\N{Large Green Circle}"
FIVE = "\N{Large Orange Circle}"
SIX = "\N{Large Purple Circle}"
SEVEN = "\N{Large Brown Circle}"
EIGHT = "\N{Medium Black Circle}"
NINE = "\N{Medium White Circle}"
CANCEL = "\N{SQUARED CL}"
ERROR = "\N{WARNING SIGN}"
# リアクションリスト
REACTION_LIST = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE]


# help_Embed
help = discord.Embed(
    title="募集用bot 「@bot_chan」の使い方",
    description="募集したい内容を、人数を設定して募集をかけることが出きるbotです。\n" "各コマンドの使い方は以下を御参照ください。\n",
    color=discord.Color.green(),
)
# help ?at使い方
help.add_field(
    name=":loudspeaker: 各コマンドの使い方\n",
    value=":pushpin:***募集を募るコマンド***\n"
    "   募集の際に使うこのbotの基本となるコマンド\n"
    "\n"
    "   ***記述方法***\n"
    "   **" + Emcompre + "at 「募集要項」 「人数」**\n"
    "\n"
    "   ※各要素に必ず半角スペースを１つ設けてください。\n"
    "   ※鍵かっこをつける必要はありません。\n"
    "   ※合計９人まで募集をかけられます。\n"
    "   ※それぞれの参加ボタンが押された時点で募集を終了します。\n"
    "\n"
    ":pushpin:***バグ対応用コマンド***\n"
    "   コマンド実行時などにバグが発生した際に一時的な対策として使うコマンド\n"
    "\n"
    "   ***記述方法***\n"
    "   **" + Emcompre + "atre**\n",
    inline=False,
)
# help リアクションについて
help.add_field(
    name=":loudspeaker: リアクションについて\n",
    value="このbotではリアクションを用いて\n"
    "__参加ボタン__を(例 :red_circle:)\n"
    "__募集中止ボタン__を(:cl:)として扱っています。\n"
    "\n"
    ":pushpin:参加ボタンについて\n"
    "   人数に応じてボタンが追加されます。\n"
    "   募集者や一度リアクションした人はボタンを押せなくなります。\n"
    "\n"
    ":pushpin:募集中止ボタンについて\n"
    "   募集中止ボタンは押した時点で__募集を取り消す__ことができます。\n",
)
# help developper info
help.set_footer(
    text="made by Farrule\n" "@bot_chan verstion: @bot_chan " + botver,
    icon_url="https://cdn.discordapp.com/"
    "attachments/865123798813900820/865258524971106314/Farrule_logo2.jfif",
)

# update_Embed
# TODO: バージョンアップ時変更
update = discord.Embed(title="アップデート内容", color=discord.Color.red())
update.add_field(
    name=":wrench: ver" + botver + "アップデート\n",
    value="プログラムの根幹部分を最適化\n"
    "プログラムの修正を簡易化\n"
    "!upコマンドの追加\n"
    "!helpコマンドのコマンド名をを!hpに変更\n",
)
update.set_footer(text="date 25, 7, 2021")


def resetter():  # 要素リセット
    global flag, MEMBER_LIST, MEMBER_DIS, b_count, o_flag, m_count
    flag = True
    b_count = 0
    o_flag = 0
    m_count = 0
    MEMBER_LIST = []
    MEMBER_DIS = []


@bot.event  # ? 起動時処理
async def on_ready():
    print("-----------------------------------------------------\n")
    print("run")
    print("BotN")
    print("Farrule")
    print(discord.__version__)
    print(sys.version + "\n")
    print("-----------------------------------------------------")
    await bot.change_presence(activity=discord.Game(name="!at 募集内容 人数 |"))


# ? up コマンド入力処理
@bot.command()
async def up(ctx):
    await ctx.send(embed=update)


# ? help コマンド入力時処理
@bot.command()
async def hp(ctx):
    await ctx.send(embed=help)


# ? atre コマンド入力時処理
@bot.command()
async def atre(ctx):
    resetter()
    await ctx.send(":exclamation: リセット処理を実行\n")


# ? at コマンド入力時処理
@bot.command()
async def at(ctx, game, mem):
    global flag, bot_name, m, member_count, bot_mes, game_title

    if flag is True:
        if re.compile(r"\d+").search(mem):
            m = int(mem)  # 人数入力用
            member_count = m
            game_title = game
            if m <= 9:
                host = ctx.author.name
                MEMBER_LIST.append(host)
                MEMBER_DIS = ",    ".join(MEMBER_LIST)
                bot_mes = await ctx.send(
                    f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{mem}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                for x in range(m):
                    await bot_mes.add_reaction(REACTION_LIST[x])
                await bot_mes.add_reaction(CANCEL)
                bot_name = bot_mes.author.name
                flag = False
            else:
                await ctx.send(":warning:  __９人以上__の募集はできません。\n")
        else:
            await ctx.send(":warning:  __人数の項目__が不適切です。\n")
    else:
        await ctx.send(":warning:  __募集中__の要項があります。\n")


# ? リアクションボタン メンバーリスト追加処理
@bot.event
async def on_reaction_add(reaction, user):
    global MEMBER_LIST, o_flag, m_count, m
    reaction

    if m_count >= m + 1:
        user = user.name
        if user in MEMBER_LIST:
            # print(user)
            o_flag = False
            # print(o_flag)
            return o_flag
        else:
            # print(user)
            o_flag = True
            MEMBER_LIST.append(user)
            return o_flag
    else:
        m_count += 1
        return m_count


# ? 各リアクション処理
@bot.event
async def on_raw_reaction_add(reaction):
    global b_count, o_flag

    # 募集人数カウンタ
    def mem_counter():
        global member_count
        m_c = int(member_count)
        m_c -= 1
        member_count = str(m_c)
        return member_count

    # メンバーリスト整列
    def mem_sort():
        global MEMBER_LIST, MEMBER_DIS
        if bot_name in MEMBER_LIST:
            MEMBER_LIST.remove(bot_name)
        MEMBER_DIS = ",    ".join(MEMBER_LIST)

    if b_count >= m + 1:
        # ! CANCELボタン処理
        if reaction.emoji.name == CANCEL:
            # print('runCANCEL')
            await bot_mes.clear_reaction(CANCEL)
            for y in range(m):
                await bot_mes.clear_reaction(REACTION_LIST[y])
            await bot_mes.edit(content="募集が__中止__されました。\n")
            resetter()

        await asyncio.sleep(0.1)
        # ! 参加ボタン処理
        if reaction.emoji.name == ONE:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(ONE)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == TWO:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(TWO)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == THREE:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(THREE)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == FOUR:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(FOUR)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == FIVE:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(FIVE)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == SIX:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(SIX)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == SEVEN:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(SEVEN)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == EIGHT:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(EIGHT)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()

        if reaction.emoji.name == NINE:
            if o_flag is False:
                await bot_mes.add_reaction(ERROR)
                await asyncio.sleep(1)
                await bot_mes.clear_reaction(ERROR)
                o_flag = True
                return
            else:
                mem_counter()
                mem_sort()
                await bot_mes.clear_reaction(NINE)
                await bot_mes.edit(
                    content=f":loudspeaker: @here ***{game_title}*** で"
                    f" ***{member_count}*** /_{m}_ 人募集中です。\n"
                    f":pushpin: 参加者:\n       {MEMBER_DIS}"
                )
                if member_count == "0":
                    await bot_mes.clear_reaction(CANCEL)
                    mem_sort()
                    await bot_mes.edit(
                        content=f"***{game_title}*** の募集は__終了__しました。\n"
                        f":pushpin: 参加者:\n       {MEMBER_DIS}"
                    )
                    await bot_mes.channel.send("@here 準備してください。\n")
                    resetter()
    else:
        b_count += 1
        return b_count


bot.run(TOKEN)
