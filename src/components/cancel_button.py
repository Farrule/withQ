import discord # type: ignore
import logging
from discord.interactions import Interaction # type: ignore
from discord.ui import Button # type: ignore
import src.backend.db as db


class CancelButton(Button):
    def __init__(self, title: str, in_queue_member_dict: dict, is_deadline: bool, session_id: str):
        super().__init__(label="CANCEL", style=discord.ButtonStyle.grey, custom_id=f"cancel:{session_id}")
        self.title = title
        self.in_queue_member_dict = in_queue_member_dict
        self.is_deadline = is_deadline
        self.session_id = session_id

    async def callback(self, interaction: Interaction):
        # ボタン押下者が募集主の場合、募集が終了した旨を伝える募集メッセージに編集する
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            mentions = ""

            for mention in self.in_queue_member_dict.values():
                mentions += mention + ' '

            if self.is_deadline:
                self.in_queue_member_dict["is_deadline_param"] = "False"

            if self.view is not None:
                self.view.stop()

            db.delete_session(self.session_id)
            await interaction.response.edit_message(content=f'{mentions}\n{self.title}\n上記の募集は取り消されました。', view=None)
            logging.info(f"[withQ-{self.session_id}] 募集が終了しました(キャンセル)。")
            return
        # ボタン押下者が募集主ではない場合、募集を取り消すことができない旨を伝えるメッセージを送信する
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を取り消すことができるのは募集主のみです。", ephemeral=True)
            return
