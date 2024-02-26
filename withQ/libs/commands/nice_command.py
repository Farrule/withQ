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

        # 音声ファイルを読み込み
        player = voice_client.play(discord.FFmpegPCMAudio(audio_file))

        print("aaa")

        # 再生完了時にメッセージを送信
        def on_end():
            player.stop()
            voice_client.disconnect()

        player.on_end(on_end)

        return

    except Exception as e:
        await interaction.response.send_message(content="コマンドの実行に失敗しました", ephemeral=True)
        logging.basicConfig(
            format='%(asctime)s %(message)s', level=logging.INFO)
        logging.error(f'Error: {e}')
        return
