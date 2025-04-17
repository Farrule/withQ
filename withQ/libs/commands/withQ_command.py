import asyncio
import datetime
import logging
import pytz

import discord
from discord.interactions import Interaction

import withQ.libs.components.deadline_time as dt
import withQ.libs.components.row_view as row_view
import withQ.libs.constants.const as c


async def command(tree, interaction: discord.Interaction, title, recruitment_num, deadline_time, mention_target, feedback, env_c):
    try:
        now_datetime = datetime.datetime.now()
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
            is_deadline = True

        # ログ出力
        #print(f"withQ_command: title: {title}, recruitment_num: {recruitment_num}, now_datetime: {now_datetime}, deadline_time: {deadline_time}, mention_target: {mention_target}, feedback: {feedback}")
        logging.info(f"withQ_command: title: {title}, recruitment_num: {recruitment_num}, now_datetime: {now_datetime}, deadline_time: {deadline_time}, total_seconds: {total_seconds}, is_deadline: {is_deadline}, mention_target: {mention_target}, feedback: {feedback}")

        # 募集メッセージを作成、送信する
        try:
            await interaction.response.send_message(
                content=f'{mention_target}\n{title}  @{recruitment_num} {"締切時間:" + deadline_time if deadline_time != None else ""}\n募集者: {next(iter(in_queue_member_dict))}\n参加者:',
                view=row_view.RowView(
                    title,
                    recruitment_num,
                    in_queue_member_dict,
                    recruiter,
                    mention_target,
                    feedback,
                    deadline_time,
                    is_deadline,
                )
            )
        except Exception as e:
            await interaction.response.send_message("コマンドの実行に失敗しました")
            logging.error(f'Error: {e}')
            return

        # 締め切り処理
        if total_seconds > 0:
            await asyncio.sleep(total_seconds)
            if "False" != in_queue_member_dict[next(iter(reversed(in_queue_member_dict)))]:
                # 募集に参加した人がいなかった場合
                if len(in_queue_member_dict) <= 1:
                    await interaction.edit_original_response(
                        content=f'{title}\n上記の募集は成立しませんでした。',
                        view=None,
                    )
                    return
                # 募集に参加した人がいた場合
                if len(in_queue_member_dict) >= 1:
                    mentions = ""
                    for mention in in_queue_member_dict.values():
                        mentions += mention + ' '
                    await interaction.edit_original_response(
                        content=f'{mentions}\n{title}  {deadline_time}\n{c.DEADLINE_TEXT}になりましたので上記の募集を締め切りました。',
                        view=None,
                    )
                    return

    except Exception as e:
        await interaction.response.send_message(content="コマンドの実行に失敗しました", ephemeral=True)
        logging.error(f'Error: {e}')
        return
