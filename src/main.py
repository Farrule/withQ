import os
from typing import Optional

import discord
from discord import app_commands
from dotenv import load_dotenv

# get bot TOKEN from ./env file
load_dotenv(verbose=True)
TOKEN = os.getenv("TOKEN")

# instance
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# startup process
@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("------")


# /add command
@tree.command()
@app_commands.describe(
    first_value="The first value you want to add something to",
    second_value="The value you want to add to the first value",
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(
        f"{first_value} + {second_value} = {first_value + second_value}"
    )


client.run(TOKEN)
