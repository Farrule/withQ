import discord
from discord.ui import Button, View
from discord.interactions import Interaction


class CancelButton(Button):
    def __init__(self, in_queue_member_dict: dict):
        super().__init__(label="CANCEL", style=discord.ButtonStyle.grey)
        self.in_queue_member_dict = in_queue_member_dict

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        # ボタン押下者が募集主の場合、募集が終了した旨を伝える募集メッセージに編集する
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            await interaction.response.edit_message(content="この募集は終了しました。", view=None)
            return
        # ボタン押下者が募集主ではない場合、募集を取り消すことができない旨を伝えるメッセージを送信する
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を取り消すことができるのは募集主のみです。", ephemeral=True)
            return
