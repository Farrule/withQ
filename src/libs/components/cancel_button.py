import discord
from discord.interactions import Interaction
from discord.ui import Button


class CancelButton(Button):
    def __init__(self, title: str, in_queue_member_dict: dict, is_deadline: bool):
        super().__init__(label="CANCEL", style=discord.ButtonStyle.grey)
        self.title = title
        self.in_queue_member_dict = in_queue_member_dict
        self.is_deadline = is_deadline

    async def callback(self, interaction: Interaction):
        # ボタン押下者が募集主の場合、募集が終了した旨を伝える募集メッセージに編集する
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            mentions = ""
            for mention in self.in_queue_member_dict.values():
                mentions += mention + ' '
            if self.is_deadline:
                self.in_queue_member_dict["is_deadline_param"] = "False"
            await interaction.response.edit_message(content=f'{mentions}\n{self.title}\n上記の募集は取り消されました。', view=None)
            return
        # ボタン押下者が募集主ではない場合、募集を取り消すことができない旨を伝えるメッセージを送信する
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を取り消すことができるのは募集主のみです。", ephemeral=True)
            return
