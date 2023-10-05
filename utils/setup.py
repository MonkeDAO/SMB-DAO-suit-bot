from config import bot
import discord

async def set_up():
    await bot.wait_until_ready()
    guild = bot.get_guild(874638621368533012)
    chan = guild.get_channel(1152345132914462810)
    index = 0
    async for message in chan.history(limit=300):
        message: discord.Message
        index += 1
        for reaction in message.reactions:
            async for user in reaction.users():
                if user.bot: continue
                if isinstance(user, discord.User): 
                    continue
                if 1123193060982001674 not in [role.id for role in user.roles]:
                    await reaction.remove(user)