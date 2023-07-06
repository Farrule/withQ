import discord
from discord.ui import Button, View
from discord.interactions import Interaction

class InQButton(Button):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict):
        super().__init__(label="IN Q", style=discord.ButtonStyle.primary)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: View = self.view
        print(view.is_finished())
        print(self.in_queue_member_dict)
        # ボタン押下者が対象の募集に参加していない場合、メンションリストとユーザーリストにボタン押下者の情報を追加する
        if interaction.user.global_name not in self.in_queue_member_dict:
            self.in_queue_member_dict[interaction.user.global_name] = interaction.user.mention
            print(self.in_queue_member_dict)
            # 募集人数に達した場合、参加者リストの参加者にメンションし募集が完了した旨を伝えるメッセージを送信する
            if len(self.in_queue_member_dict) - 1 == self.recruitment_num:
                mentions = ""
                for mention in self.in_queue_member_dict.values():
                    mentions += mention
                await interaction.response.edit_message(
                    content=f'{mentions}\n{self.title}\n上記の募集が完了しました。',
                    view=None,
                )
                return
            # 募集人数に達していない場合、募集用メッセージを編集し残りの募集人数を変更する
            if len(self.in_queue_member_dict) <= self.recruitment_num:
                users = ""
                for user in self.in_queue_member_dict:
                    if user != next(iter(self.in_queue_member_dict)):
                        users = user + ',' + users
                await interaction.response.edit_message(
                    content=f'{self.title}  @{self.recruitment_num - len(self.in_queue_member_dict) + 1}\n募集者: {next(iter(self.in_queue_member_dict))}\n参加者: {users}'
                )
                await interaction.followup.send("この募集に参加しました。", ephemeral=True)
                print(self.in_queue_member_dict)
        # ボタン押下者が対象の募集にすでに参加している場合、その旨を伝えるメッセージを送信する
        elif interaction.user.global_name in self.in_queue_member_dict:
            await interaction.response.send_message("すでにこの募集に参加しています。", ephemeral=True)
            print(self.in_queue_member_dict)