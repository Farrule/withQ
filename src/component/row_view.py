from discord.ui import View

import component.in_q_button as in_q_button
import component.de_q_button as de_q_button
import component.closing_q_button as closing_button
import component.cancel_button as cancel_button

class RowView(View):
    def __init__(self, title: str, recruitment_num: int, in_queue_member_dict: dict):
        super().__init__(timeout=None)
        self.add_item(in_q_button.InQButton(title, recruitment_num, in_queue_member_dict))
        self.add_item(de_q_button.DeQButton(title, recruitment_num, in_queue_member_dict))
        self.add_item(closing_button.ClosingQButton(title, recruitment_num, in_queue_member_dict))
        self.add_item(cancel_button.CancelButton(in_queue_member_dict))