import discord
from discord import app_commands
from discord.ext import commands
import traceback
from config import bot, dc_tk
import asyncio
import logging
from aiohttp import web
from commands.dress_up import dressup #type: ignore
from tasks.tasks import update_gen3
from web.web import app

logging.basicConfig(level=logging.INFO)

async def run_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 8080)
    await site.start()

def error_handler(task: asyncio.Task):
    exc = task.exception()
    if exc:
        traceback.print_exception(type(exc), exc, exc.__traceback__)

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
    if update_gen3.is_running():
        update_gen3.restart()
    else:
        update_gen3.start()

@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    print("test")
    await bot.tree.sync()

async def main():
    async with bot:
        web = bot.loop.create_task(run_server())
        web.add_done_callback(error_handler)
        await bot.start(dc_tk)

asyncio.run(main())