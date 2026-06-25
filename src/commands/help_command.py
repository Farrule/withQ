import logging

import discord

import components.help_embed as help_embed


async def command(tree, interaction: discord.Interaction):
    try:
        await interaction.response.send_message(
            embed=help_embed.embed,
            ephemeral=True
        )
        logging.info("help_command: success")
        return
    except Exception as e:
        await interaction.response.send_message("コマンドの実行に失敗しました", ephemeral=True)
        logging.error(f'Error: {e}')
        return
