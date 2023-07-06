import discord
from discord.ui import Button, View
from discord.interactions import Interaction

class DeQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict):
        super().__init__(label="DE Q", style=discord.ButtonStyle.red)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        print(self.in_queue_member_dict)
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message("募集主はDE Qできません。", ephemeral=True)
            return
        if interaction.user.global_name in self.in_queue_member_dict:
            self.in_queue_member_dict.pop(interaction.user.global_name)
            users = ""
            for user in self.in_queue_member_dict:
                if user != next(iter(self.in_queue_member_dict)):
                    users = user + ',' + users
            await interaction.response.edit_message(
                content=f'{self.title}  @{self.recruitment_num - len(self.in_queue_member_dict) + 1}\n募集者: {next(iter(self.in_queue_member_dict))}\n参加者: {users}'
            )
            await interaction.followup.send("この募集への参加を取り消しました。", ephemeral=True)
            print(self.in_queue_member_dict)
        elif interaction.user.global_name not in self.in_queue_member_dict.keys():
            await interaction.response.send_message("あなたはこの募集に参加していません。", ephemeral=True)
            print(self.in_queue_member_dict)