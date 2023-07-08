import discord
from discord.ui import View

import components.cancel_button as cancel_button
import components.closing_q_button as closing_button
import components.de_q_button as de_q_button
import components.in_q_button as in_q_button


class RowView(View):
    def __init__(
        self,
        title: str,
        recruitment_num: int,
        in_queue_member_dict: dict,
        recruiter: discord.member.Member,
        mention_target: str,
        is_feedback_on_recruitment: bool,
        deadline_time: str,
        is_deadline: bool,
    ):
        super().__init__(timeout=None)
        self.add_item(in_q_button.InQButton(
            title, recruitment_num, in_queue_member_dict, recruiter, mention_target, is_feedback_on_recruitment, deadline_time))
        self.add_item(de_q_button.DeQButton(
            title, recruitment_num, in_queue_member_dict, recruiter, mention_target, is_feedback_on_recruitment, deadline_time))
        self.add_item(closing_button.ClosingQButton(
            title, recruitment_num, in_queue_member_dict, deadline_time, is_deadline))
        self.add_item(cancel_button.CancelButton(
            in_queue_member_dict, is_deadline))
