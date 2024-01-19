import discord
from discord.interactions import Interaction
from discord.ui import Button


class ClosingQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict, deadline_time: str, is_deadline: bool):
        super().__init__(label="〆", style=discord.ButtonStyle.green)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict
        self.deadline_time = deadline_time
        self.is_deadline = is_deadline

    async def callback(self, interaction: Interaction):
        # ボタン押下者が募集主の場合、募集メッセージを編集して募集を締め切った旨を伝えるメッセージにする
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            mentions = ""
            for mention in self.in_queue_member_dict.values():
                mentions += mention + ' '
            if self.is_deadline:
                self.in_queue_member_dict["is_deadline_param"] = "False"
            await interaction.response.edit_message(
                content=f'{mentions}\n{self.title} {self.deadline_time if self.deadline_time != None else ""}\n上記の募集を締め切りました。',
                view=None,
            )
            return
        # ボタン押下者が募集主ではない場合、募集を取り消すことができない旨を伝えるメッセージを送信する
        elif interaction.user.global_name != next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message(content="募集を締め切ることができるのは募集主のみです。", ephemeral=True)
            return
