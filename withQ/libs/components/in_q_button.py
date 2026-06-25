import discord
import logging
from discord.interactions import Interaction
from discord.ui import Button


class InQButton(Button):
    def __init__(
        self,
        title: str,
        recruitment_num: int,
        in_queue_member_dict: dict,
        recruiter: discord.member.Member,
        mention_target: str,
        is_feedback_on_recruitment: bool,
        deadline_time: str,
        session_id: str
    ):
        super().__init__(label="IN Q", style=discord.ButtonStyle.primary)
        self.title = title
        self.recruitment_num = recruitment_num
        self.in_queue_member_dict = in_queue_member_dict
        self.recruiter = recruiter
        self.mention_target = mention_target
        self.is_feedback_on_recruitment = is_feedback_on_recruitment
        self.deadline_time = deadline_time
        self.session_id = session_id

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        # ボタン押下者が対象の募集に参加していない場合、参加者ディクショナリにボタン押下者の情報を追加する
        if interaction.user.global_name not in self.in_queue_member_dict:
            self.in_queue_member_dict[interaction.user.global_name] = interaction.user.mention
            # 募集人数に達した場合、参加者リストの参加者にメンションし募集が完了した旨を伝えるメッセージを送信する
            if len(self.in_queue_member_dict) - 1 == self.recruitment_num:
                mentions = ""
                for mention in self.in_queue_member_dict.values():
                    mentions += mention + ' '
                if self.view is not None:
                    self.view.stop()
                await interaction.response.edit_message(
                    content=f'{mentions}\n{self.title}\n上記の募集が完了しました。',
                    view=None,
                )
                members = [k for k in self.in_queue_member_dict.keys() if k != "is_deadline_param"]
                logging.info(f"[withQ-{self.session_id}] 募集が完了しました(満員)。 最終参加者: {members}, 募集人数: {self.recruitment_num}")
                return

            # 募集人数に達していない場合、募集用メッセージを編集する
            if len(self.in_queue_member_dict) <= self.recruitment_num:
                users = ""
                for user in self.in_queue_member_dict:
                    if user != next(iter(self.in_queue_member_dict)):
                        users = user + ',' + users
                await interaction.response.edit_message(
                    content=f'{self.mention_target}\n{self.title}  @{self.recruitment_num - len(self.in_queue_member_dict) + 1} {self.deadline_time if self.deadline_time != None else ""}\n募集者: {next(iter(self.in_queue_member_dict))}\n\参加者: {users}'
                )
                await interaction.followup.send("この募集に参加しました。", ephemeral=True)
                members = [k for k in self.in_queue_member_dict.keys() if k != "is_deadline_param"]
                logging.info(f"[withQ-{self.session_id}] ユーザーが参加しました。 ユーザー: {interaction.user.global_name}, 現在の参加者: {members}")
                if self.is_feedback_on_recruitment:
                    await self.recruiter.send(
                        content=f'あなたが募集している {self.title} に {interaction.user.global_name} が参加しました。',
                    )
                return
        # ボタン押下者が対象の募集にすでに参加している場合、その旨を伝えるメッセージを送信する
        elif interaction.user.global_name in self.in_queue_member_dict:
            await interaction.response.send_message("すでにこの募集に参加しています。", ephemeral=True)
            return
