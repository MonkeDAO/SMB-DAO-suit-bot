import discord
from discord import app_commands
from discord.ext import commands
import traceback
from config import bot, dc_tk
import asyncio
import logging
from commands.dress_up import dressup #type: ignore
from commands.banner import banner #type: ignore
from tasks.tasks import update_gen3
from utils.setup import set_up

logging.basicConfig(level=logging.INFO)

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

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.channel_id != 1152345132914462810: return
    guild = bot.get_guild(payload.guild_id)
    if not guild: return
    member = guild.get_member(payload.user_id)
    if not member: return
    if member.bot: return
    msg = guild.get_channel(payload.channel_id).get_partial_message(payload.message_id)
    if not msg: return
    if 1123193060982001674 not in [role.id for role in member.roles]: 
        await msg.remove_reaction(payload.emoji, member)
        return

@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):
    print("test")
    await bot.tree.sync()

async def main():
    async with bot:
        resuming_views = bot.loop.create_task(set_up())
        resuming_views.add_done_callback(error_handler)
        await bot.start(dc_tk)

asyncio.run(main())