import sys
sys.path.append('..')
import discord
from config import bot

@bot.tree.command(name="test")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("test")