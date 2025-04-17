import logging

import discord


async def command(tree, interaction: discord.Interaction):
    try:
        await tree.fetch_commands()
        await interaction.response.send_message("コマンドの更新に成功しました", ephemeral=True)

        logging.info("update_command: seccess")

        return
    except Exception as e:
        await interaction.response.send_message("コマンドの更新に失敗しました", ephemeral=True)
        logging.error(f'Error: {e}')
        return
