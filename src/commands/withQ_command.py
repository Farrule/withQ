import asyncio
import datetime
import logging
import uuid
import pytz # type: ignore

import discord # type: ignore
from discord.interactions import Interaction # type: ignore

import src.components.deadline_time as dt
import src.components.row_view as row_view
import src.constants.const as c


import src.backend.db as db

async def monitor_deadline(client, session_id, view, total_seconds, title, deadline_time, in_queue_member_dict, channel_id, message_id):
    try:
        elapsed = 0
        while elapsed < total_seconds:
            if view.is_finished():
                return
            await asyncio.sleep(1)
            elapsed += 1

        if not view.is_finished():
            view.stop()
            db.delete_session(session_id)

            channel = client.get_channel(channel_id) or await client.fetch_channel(channel_id)
            if not channel:
                return
            try:
                message = await channel.fetch_message(message_id)
            except discord.NotFound:
                return

            # 募集に参加した人がいなかった場合
            if len(in_queue_member_dict) <= 1:
                await message.edit(
                    content=f'{title}\n上記の募集は成立しませんでした。',
                    view=None,
                )
                logging.info(f"[withQ-{session_id}] 募集が終了しました(時間切れ・不成立)。")
                return
            # 募集に参加した人がいた場合
            if len(in_queue_member_dict) >= 1:
                mentions = ""
                for mention in in_queue_member_dict.values():
                    mentions += mention + ' '
                await message.edit(
                    content=f'{mentions}\n{title}  {deadline_time if deadline_time is not None else ""}\n{c.DEADLINE_TEXT}になりましたので上記の募集を締め切りました。',
                    view=None,
                )
                members = [k for k in in_queue_member_dict.keys() if k != "is_deadline_param"]
                logging.info(f"[withQ-{session_id}] 募集が完了しました(時間切れ・成立)。 最終参加者: {members}")
                return
    except Exception as e:
        logging.error(f"Error in monitor_deadline for {session_id}: {e}")

async def command(tree, interaction: discord.Interaction, title, recruitment_num, deadline_time, mention_target, feedback, env_c):
    try:
        now_datetime = datetime.datetime.now()
        session_id = uuid.uuid4().hex[:8]
        # key: 参加者ユーザーネーム value:メンションID 初期値として募集者を代入
        in_queue_member_dict = {
            interaction.user.global_name: interaction.user.mention
        }
        recruiter = interaction.user
        is_deadline = False


        # 募集人数が1人以上でない場合、returnする
        if recruitment_num <= 0:
            await interaction.response.send_message(content='募集人数の数値が正しくありません', ephemeral=True)
            return

        # mention_targetオプションが指定されていない場合に値を空文字列に変換する
        if mention_target == None:
            mention_target = ""

        # 開始時間時間が指定されている場合に締め切り時間の計算処理を行う
        if deadline_time != None:
            total_seconds, deadline_time, is_deadline = dt.deadline_time(
                deadline_time, now_datetime)

        # 開始時間が設定されていない場合、締め切り時間を設定する
        elif deadline_time == None:
            total_seconds = env_c.AUTO_DEADLINE
            is_deadline = False
            auto_deadline_datetime = now_datetime + datetime.timedelta(seconds=total_seconds)
            if auto_deadline_datetime.date() == now_datetime.date():
                deadline_time = auto_deadline_datetime.strftime("%H:%M")
            else:
                deadline_time = auto_deadline_datetime.strftime("%m/%d/%H:%M")

        # ログ出力
        #print(f"withQ_command: title: {title}, recruitment_num: {recruitment_num}, now_datetime: {now_datetime}, deadline_time: {deadline_time}, mention_target: {mention_target}, feedback: {feedback}")
        logging.info(f"[withQ-{session_id}] 募集を開始しました。 募集者: {recruiter.global_name}, タイトル: {title}, 募集人数: {recruitment_num}, 締め切り時間: {deadline_time if deadline_time != None else 'AUTO_DEADLINE'}")

        # 募集メッセージを作成、送信する
        view = row_view.RowView(
            title,
            recruitment_num,
            in_queue_member_dict,
            recruiter,
            mention_target,
            feedback,
            deadline_time,
            is_deadline,
            session_id,
        )
        try:
            deadline_text = f"\n締切時間:{deadline_time}" if (is_deadline and deadline_time is not None) else ""

            await interaction.response.send_message(
                content=f'{mention_target}\n{title}  @{recruitment_num}{deadline_text}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=view
            )
            message = await interaction.original_response()

            # SQLiteにセッションを保存
            expire_at = None
            if total_seconds > 0:
                expire_at = (now_datetime + datetime.timedelta(seconds=total_seconds)).isoformat()

            db.save_session(
                session_id=session_id,
                title=title,
                recruitment_num=recruitment_num,
                in_queue_member_dict=in_queue_member_dict,
                recruiter_id=recruiter.id,
                recruiter_global_name=recruiter.global_name,
                mention_target=mention_target,
                is_feedback_on_recruitment=feedback,
                deadline_time=deadline_time,
                is_deadline=is_deadline,
                guild_id=interaction.guild_id,
                channel_id=interaction.channel_id,
                message_id=message.id,
                expire_at=expire_at
            )
        except Exception as e:
            logging.error(f'Error: {e}')
            if interaction.response.is_done():
                await interaction.followup.send(content="コマンドの実行に失敗しました", ephemeral=True)
            else:
                await interaction.response.send_message(content="コマンドの実行に失敗しました", ephemeral=True)
            return

        # 締め切り処理
        if total_seconds > 0:
            asyncio.create_task(monitor_deadline(
                client=interaction.client,
                session_id=session_id,
                view=view,
                total_seconds=total_seconds,
                title=title,
                deadline_time=deadline_time,
                in_queue_member_dict=in_queue_member_dict,
                channel_id=interaction.channel_id,
                message_id=message.id
            ))

    except Exception as e:
        logging.error(f'Error: {e}')
        if interaction.response.is_done():
            await interaction.followup.send(content="コマンドの実行に失敗しました", ephemeral=True)
        else:
            await interaction.response.send_message(content="コマンドの実行に失敗しました", ephemeral=True)
        return
