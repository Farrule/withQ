import discord # type: ignore
import logging
from discord.interactions import Interaction # type: ignore
from discord.ui import Button # type: ignore
import src.backend.db as db


class ClosingQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict, deadline_time: str, is_deadline: bool, session_id: str):
        super().__init__(label="〆", style=discord.ButtonStyle.green, custom_id=f"closing:{session_id}")
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict
        self.deadline_time = deadline_time
        self.is_deadline = is_deadline
        self.session_id = session_id

    async def callback(self, interaction: Interaction):
        # ボタン押下者が募集主の場合、募集メッセージを編集して募集を締め切った旨を伝えるメッセージにする
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            mentions = ""
            for mention in self.in_queue_member_dict.values():
                mentions += mention + ' '
            if self.is_deadline:
                self.in_queue_member_dict["is_deadline_param"] = "False"

            if self.view is not None:
                self.view.stop()

            db.delete_session(self.session_id)

            deadline_text = f"\n締切時間:{self.deadline_time}" if (self.is_deadline and self.deadline_time is not None) else ""

            await interaction.response.edit_message(
                content=f'{mentions}\n{self.title} {deadline_text}\n上記の募集を締め切りました。',
                view=None,
            )
            members = [k for k in self.in_queue_member_dict.keys() if k != "is_deadline_param"]
            logging.info(f"[withQ-{self.session_id}] 募集が完了しました(手動締め切り)。 最終参加者: {members}")
            return
        # ボタン押下者が募集主ではない場合、募集を取り消すことができない旨を伝えるメッセージを送信する
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を締め切ることができるのは募集主のみです。", ephemeral=True)
            return
