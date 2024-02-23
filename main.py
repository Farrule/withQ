import os
from os.path import dirname, join

import discord
from discord import app_commands
from dotenv import load_dotenv

import withQ.libs.commands.help_command as HelpCommand
import withQ.libs.commands.random_command as RandomCommand
import withQ.libs.commands.update_command as UpdateCommand
import withQ.libs.commands.withQ_command as WithQCommand
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

# bot初期化
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(command_prefix='/', intents=intents)
tree = app_commands.CommandTree(client)


# client起動時にステータスメッセージを変更してclientの情報を出力する
@client.event
async def on_ready():
    await client.change_presence(activity=discord.CustomActivity(name="In Q with your friends!"))
    print(f"Logged in as {client.user} (ID: {client.user.id})")

    # コマンドツリーの同期
    try:
        await tree.sync()
        print("Update success!")
    except Exception as e:
        print("Update failure!")
        print(e)

    print("------")


# botがサーバーに参加した時にコマンドを同期する
@client.event
async def on_guild_join(guild):
    await tree.sync()


# botがサーバーを退出したときににコマンドを削除する
@client.event
async def on_guild_remove(guild):
    await tree.clear_commands(guild.id, type=None)


# /update コマンドツリーの更新を行うコマンド
@tree.command(
    name="update",
    description="withQのコマンドを更新します"
)
async def update_command(interaction: discord.Interaction):
    await UpdateCommand.command(tree, interaction)


# /help embedをコマンド入力者に送信する
@tree.command(
    name="help",
    description="withQのヘルプコマンド"
)
async def help_command(interaction: discord.Interaction):
    await HelpCommand.command(tree, interaction)


# /withQ 募集を実施するコマンド
@app_commands.choices(
    mention_target=[
        discord.app_commands.Choice(name="everyone", value="@everyone"),
        discord.app_commands.Choice(name="here", value="@here"),
    ]
)
@tree.command(
    name="withq",
    description="募集内容や人数、時間を指定して募集を開始します"
)
async def withQ_command(
    interaction: discord.Interaction,
    title: str,
    recruitment_num: int,
    deadline_time: str = None,
    mention_target: str = None,
    feedback: bool = True,
):
    await WithQCommand.command(
        tree,
        interaction,
        title,
        recruitment_num,
        deadline_time,
        mention_target,
        feedback,
        env_c,
    )


# /random 入力された候補値からランダムに値を返すコマンド
@app_commands.describe(
    candidate="候補値の間にスペースを入れてください",
)
@tree.command(
    name="random",
    description="入力された候補からランダムに選出するコマンド"
)
async def random_command(
    interaction: discord.Integration,
    candidate: str
):
    await RandomCommand.command(
        tree,
        interaction,
        candidate,
    )


keep_alive()
client.run(TOKEN)
