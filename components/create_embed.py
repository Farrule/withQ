import discord
import markdown

def create_embed(filename):
    with open(filename, "r") as f:
        md = f.read()

    parsed = markdown.markdown(md)
    embed = discord.Embed(title=filename, description=parsed)

    return embed
