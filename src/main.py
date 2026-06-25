import os
import logging
from os.path import dirname, join
import datetime
import asyncio

import discord
from discord import app_commands

import commands.help_command as HelpCommand
import commands.random_command as RandomCommand
import commands.update_command as UpdateCommand
import commands.withQ_command as WithQCommand

import components.row_view as row_view

import database.db as db

from config.settings import env_c, TOKEN

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

if env_c.DEBUG_MODE:
    logging.info('Service Status: DEBUG')
else:
    logging.info('Service Status: PRODUCTION')

# bot初期化
intents = discord.Intents.all()
intents.message_content = True
allowed = discord.AllowedMentions.all()
client = discord.Client(intents=intents, allowed_mentions=allowed)
tree = app_commands.CommandTree(client)


# client起動時にステータスメッセージを変更してclientの情報を出力する
@client.event
async def on_ready():
    await client.change_presence(activity=discord.CustomActivity(name="In Q with your friends!"))
    logging.info(f"Logged in as {client.user} (ID: {client.user.id})")

    # コマンドツリーの同期
    try:
        await tree.sync()
        logging.info("Update success!")
    except Exception as e:
        logging.info("Update failure!")
        logging.error(e)

    # データベースの初期化とアクティブセッションの復元
    db.init_db()
    active_sessions = db.get_active_sessions()
    logging.info(f"Restoring {len(active_sessions)} active sessions...")
    for session in active_sessions:
        try:
            recruiter = client.get_user(session["recruiter_id"])
            if recruiter is None:
                try:
                    recruiter = await client.fetch_user(session["recruiter_id"])
                except Exception:
                    recruiter = discord.Object(id=session["recruiter_id"])

            view = row_view.RowView(
                title=session["title"],
                recruitment_num=session["recruitment_num"],
                in_queue_member_dict=session["in_queue_member_dict"],
                recruiter=recruiter,
                mention_target=session["mention_target"],
                is_feedback_on_recruitment=session["is_feedback_on_recruitment"],
                deadline_time=session["deadline_time"],
                is_deadline=session["is_deadline"],
                session_id=session["session_id"]
            )
            client.add_view(view)

            if session["expire_at"]:
                expire_datetime = datetime.datetime.fromisoformat(session["expire_at"])
                now_datetime = datetime.datetime.now()
                if expire_datetime > now_datetime:
                    remaining_seconds = (expire_datetime - now_datetime).total_seconds()
                else:
                    remaining_seconds = 0

                asyncio.create_task(WithQCommand.monitor_deadline(
                    client=client,
                    session_id=session["session_id"],
                    view=view,
                    total_seconds=remaining_seconds,
                    title=session["title"],
                    deadline_time=session["deadline_time"],
                    in_queue_member_dict=session["in_queue_member_dict"],
                    channel_id=session["channel_id"],
                    message_id=session["message_id"]
                ))
            logging.info(f"Restored session: {session['session_id']}")
        except Exception as e:
            logging.info(f"Failed to restore session {session.get('session_id')}: {e}")

    logging.info("------")


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
@app_commands.describe(
    title="募集内容を入力してください",
    recruitment_num="募集人数を入力してください",
    deadline_time="締め切り時間を入力してください exp) 21:00",
    mention_target="メンション対象を選択してください",
    feedback="募集に参加者または参加辞退者が出た場合に通知を設定します"
)
@app_commands.rename(
    title="募集内容",
    recruitment_num="募集人数",
    deadline_time="締め切り時間",
    mention_target="メンション対象",
    feedback="通知設定"
)
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
    interaction: discord.Interaction,
    candidate: str
):
    await RandomCommand.command(
        tree,
        interaction,
        candidate,
    )

if __name__ == "__main__":
    if not TOKEN:
        logging.error("==================================================")
        logging.error("❌ CRITICAL ERROR: DiscordのTOKENが設定されていません!")
        logging.error("EXECUTION_ENV の値や、環境変数の設定を確認してください。")
        logging.error("==================================================")
    else:
        # TOKENが存在するときだけ実行
        client.run(TOKEN, log_handler=None)