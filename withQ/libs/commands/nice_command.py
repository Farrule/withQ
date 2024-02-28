import asyncio
import logging

import discord


async def command(tree, interaction: discord.Interaction):
    try:
        if interaction.user.voice is None:
            await interaction.response.send_message(content="コマンドの実行に失敗しました", ephemeral=True)
            return

        # ボイスチャンネルを取得
        voice_channel = interaction.user.voice.channel

        # ボイスチャンネルに接続
        voice_client = await voice_channel.connect()

        # 音声ファイルのパス
        audio_file = "./withQ/assets/nice.mp3"

        async def on_end():
            voice_client.stop()
            await voice_client.disconnect()

        # 音声ファイルを読み込み
        voice_client.play(discord.FFmpegPCMAudio(audio_file))

        await interaction.response.send_message(
            content="NICE!", ephemeral=True)

        # 再生完了を待つ
        while voice_client.is_playing():
            await asyncio.sleep(1)

        # 再生完了処理
        await on_end()

        return

    except Exception as e:
        await interaction.response.send_message(content="コマンドの実行に失敗しました", ephemeral=True)
        logging.basicConfig(
            format='%(asctime)s %(message)s', level=logging.INFO)
        logging.error(f'Error: {e}')
        return
