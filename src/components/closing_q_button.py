import discord
from discord.interactions import Interaction
from discord.ui import Button, View


class ClosingQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict, deadline_time: str):
        super().__init__(label="〆", style=discord.ButtonStyle.green)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict
        self.deadline_time = deadline_time

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        # ボタン押下者が募集主の場合、募集メッセージを編集して募集を締め切った旨を伝えるメッセージにする
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            mentions = ""
            for mention in self.in_queue_member_dict.values():
                mentions += mention + ' '
            await interaction.response.edit_message(
                content=f'{mentions}\n{self.title} {self.deadline_time if self.deadline_time != None else ""}\n上記の募集を締め切りました。',
                view=None,
            )
            return
        # ボタン押下者が募集主ではない場合、募集を取り消すことができない旨を伝えるメッセージを送信する
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を締め切ることができるのは募集主のみです。", ephemeral=True)
            return
