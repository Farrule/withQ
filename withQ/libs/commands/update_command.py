import logging

import discord


async def command(tree, interaction: discord.Interaction):
    try:
        await tree.fetch_commands()
        await interaction.response.send_message("コマンドの更新に成功しました")
        return
    except Exception as e:
        await interaction.response.send_message("コマンドの更新に失敗しました")
        logging.basicConfig(
            format='%(asctime)s %(message)s', level=logging.INFO)
        logging.error(f'Error: {e}')
        return
