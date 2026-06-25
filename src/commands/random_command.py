import logging
import random

import discord


async def command(tree, interaction: discord.Interaction, candidate: str):
    try:
        candidate_list = candidate.split()

        if not candidate_list:
            await interaction.response.send_message("候補値をスペース区切りで入力してください。", ephemeral=True)
            return

        chosen = random.choice(candidate_list)
        await interaction.response.send_message(
            f'{chosen} が選ばれました！'
        )

        logging.info("random_command: success")
        return

    except Exception as e:
        await interaction.response.send_message("コマンドの実行に失敗しました", ephemeral=True)
        logging.error(f'Error: {e}')
        return
