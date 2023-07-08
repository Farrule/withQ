import discord
from discord.interactions import Interaction
from discord.ui import Button


class DeQButton(Button):
    def __init__(
        self,
        title: str,
        recruitment_num: int,
        in_queue_member_dict: dict,
        recruiter: discord.member.Member,
        mention_target: str,
        is_feedback_on_recruitment: bool,
        deadline_time: str
    ):
        super().__init__(label="DE Q", style=discord.ButtonStyle.red)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict
        self.recruiter = recruiter
        self.mention_target = mention_target
        self.is_feedback_on_recruitment = is_feedback_on_recruitment
        self.deadline_time = deadline_time

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        # ボタン押下者が募集主の場合、参加取り消し処理を行わずに取り消しができない旨を伝えるメッセージを送信する
        if interaction.user.global_name == next(iter(self.in_queue_member_dict)):
            await interaction.response.send_message("募集主はDE Qできません。", ephemeral=True)
            return
        # ボタン押下者が参加者ディクショナリに存在する場合、参加取り消し処理を行い募集メッセージを編集し参加を取り消した旨を伝えるメッセージを送信する
        if interaction.user.global_name in self.in_queue_member_dict:
            self.in_queue_member_dict.pop(interaction.user.global_name)
            users = ""
            for user in self.in_queue_member_dict:
                if user != next(iter(self.in_queue_member_dict)):
                    users = user + ',' + users
            await interaction.response.edit_message(
                content=f'{self.mention_target}\n{self.title}  @{self.recruitment_num - len(self.in_queue_member_dict) + 1} {self.deadline_time if self.deadline_time != None else ""}\n募集者: {next(iter(self.in_queue_member_dict))}\n参加者: {users}'
            )
            await interaction.followup.send("この募集への参加を取り消しました。", ephemeral=True)
            if self.is_feedback_on_recruitment:
                await self.recruiter.send(
                    content=f'あなたが募集している {self.title} から {interaction.user.global_name} が参加を取り消しました。',
                )
            print(self.in_queue_member_dict)
            return
        # ボタン押下者が参加者ディレクトリに存在しない場合、その募集に参加していない旨を伝えるメッセージを送信する
        elif interaction.user.global_name not in self.in_queue_member_dict.keys():
            await interaction.response.send_message("あなたはこの募集に参加していません。", ephemeral=True)
            print(self.in_queue_member_dict)
            return
