import logging

import discord

import withQ.libs.constants.embed as embed


async def command(tree, interaction: discord.Interaction):
    try:
        await interaction.response.send_message(
            embed=embed.embed,
            ephemeral=True
        )
        return
    except Exception as e:
        await interaction.response.send_message("コマンドの実行に失敗しました")
        print(e)
        logging.basicConfig(
            format='%(asctime)s %(message)s', level=logging.INFO)
        logging.error(f'Error: {e}')
        return
