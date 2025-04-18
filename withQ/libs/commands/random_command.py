import logging
import random

import discord


async def command(tree, interaction: discord.Interaction, candidate: str):
    try:
        candidate_lint = candidate.split()

        await interaction.response.send_message(
            f'{candidate_lint[random.randint(0, len(candidate_lint))]} が選ばれました！'
        )

        logging.info("random_command: seccess")

        return

    except Exception as e:
        await interaction.response.send_message("コマンドの実行に失敗しました", ephemeral=True)
        logging.error(f'Error: {e}')
        return
