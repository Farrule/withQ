import discord
from discord import app_commands
from discord.ext import commands

import commands.help_command as HelpCommand
import commands.random_command as RandomCommand
import commands.update_command as UpdateCommand
import commands.withQ_command as WithQCommand
from config.settings import env_c

class AppCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # /update
    @app_commands.command(name="update", description="withQのコマンドを更新します")
    async def update_command(self, interaction: discord.Interaction):
        await UpdateCommand.command(self.bot.tree, interaction)

    # /help
    @app_commands.command(name="help", description="withQのヘルプコマンド")
    async def help_command(self, interaction: discord.Interaction):
        await HelpCommand.command(self.bot.tree, interaction)

    # /withq
    @app_commands.describe(
        title="募集内容を入力してください",
        recruitment_num="募集人数を入力してください",
        deadline_time="締め切り時間を入力してください exp) 21:00",
        mention_target="メンション対象を選択してください",
        feedback="募集に参加者または参加辞退者が出た場合に通知を設定します"
    )
    @app_commands.rename(
        title="募集内容",
        recruitment_num="募集人数",
        deadline_time="締め切り時間",
        mention_target="メンション対象",
        feedback="通知設定"
    )
    @app_commands.choices(
        mention_target=[
            app_commands.Choice(name="everyone", value="@everyone"),
            app_commands.Choice(name="here", value="@here"),
        ]
    )
    @app_commands.command(name="withq", description="募集内容や人数、時間を指定して募集を開始します")
    async def withq_command(
        self,
        interaction: discord.Interaction,
        title: str,
        recruitment_num: int,
        deadline_time: str = None,
        mention_target: str = None,
        feedback: bool = True,
    ):
        await WithQCommand.command(
            self.bot.tree, interaction, title, recruitment_num, deadline_time, mention_target, feedback, env_c
        )

    # /random
    @app_commands.describe(candidate="候補値の間にスペースを入れてください")
    @app_commands.command(name="random", description="入力された候補からランダムに選出するコマンド")
    async def random_command(self, interaction: discord.Interaction, candidate: str):
        await RandomCommand.command(self.bot.tree, interaction, candidate)

async def setup(bot: commands.Bot):
    await bot.add_cog(AppCommands(bot))