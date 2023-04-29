import discord
from discord import app_commands
from discord.ext import commands
import traceback
from config import bot, dc_tk
import asyncio
from commands.test import test #type: ignore

@bot.tree.error
async def command_errors(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    await interaction.followup.send(str(error), ephemeral=True)
    traceback.print_exception(type(error), error, error.__traceback__)
    return

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    
@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    print("test")
    await bot.tree.sync()

async def main():
    async with bot:
        await bot.start(dc_tk)

asyncio.run(main())