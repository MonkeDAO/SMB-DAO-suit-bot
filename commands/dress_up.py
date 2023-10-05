import sys
sys.path.append('..')
import discord
from discord.app_commands import Choice
from views.edit_views import DressUpViewGen2, DressUpViewGen3
from tasks.tasks import fetch_gen3_list
from config import bot, gen2List
from PIL import Image
import asyncio
from io import BytesIO
import aiohttp

@bot.tree.command(name="dress-up", description="Dress up your monke!")
async def dressup(interaction: discord.Interaction, generation: int, monke: int):
    await interaction.response.defer(ephemeral=True)
    emoji_guild = bot.get_guild(1101931928409612411)
    if (generation != 2 and generation != 3):
        await interaction.followup.send("Invalid generation", ephemeral=True)
        return
    if generation == 2:
        for i in gen2List:
            if int(i['mint']["name"].split("#")[1]) == monke:
                monke = i
                async with aiohttp.ClientSession() as session:
                    async with session.get(i['mint']['imageUri']) as resp:
                        img = await resp.read()
                        img = await asyncio.get_event_loop().run_in_executor(None, Image.open, BytesIO(img))
                break
        if type(monke) == int:
            await interaction.followup.send("The monke you tried to use could not be found", ephemeral=True)
            return
        embed = discord.Embed()
        mybytes = BytesIO()
        img.save(mybytes, format="PNG")
        mybytes.seek(0)
        file = discord.File(mybytes, filename="monke.png")
        embed.set_image(url="attachment://monke.png")
        msg = await interaction.followup.send(embed=embed, file=file)
        view = DressUpViewGen2(monke, img, msg.id, embed, emoji_guild)
        await msg.edit(view=view)
    elif generation == 3:
        gen3List = await fetch_gen3_list()
        for i in gen3List:
            if int(i["name"].split("#")[1]) == monke:
                monke = i
                async with aiohttp.ClientSession() as session:
                    async with session.get(i['imageUri']) as resp:
                        img = await resp.read()
                        img = await asyncio.get_event_loop().run_in_executor(None, Image.open, BytesIO(img))
                break
        if type(monke) == int:
            await interaction.followup.send("The monke you tried to use could not be found", ephemeral=True)
            return
        embed = discord.Embed()
        mybytes = BytesIO()
        img.save(mybytes, format="PNG")
        mybytes.seek(0)
        file = discord.File(mybytes, filename="monke.png")
        embed.set_image(url="attachment://monke.png")
        msg = await interaction.followup.send(embed=embed, file=file)
        view = DressUpViewGen3(monke, img, msg.id, embed, emoji_guild)
        await msg.edit(view=view)
        
@dressup.autocomplete("generation")
async def genauto(interaction: discord.Interaction, current: str):
    return [Choice(name="Gen 2", value="2"), Choice(name="Gen 3", value="3")]
    
@dressup.autocomplete("monke")
async def monkeeauto(interaction: discord.Interaction, current: str):
    curgen = interaction.namespace.generation
    if curgen == 2:
        allnums = range(1,5000)
        poss = [num for num in allnums if str(num).startswith(current)]
        return [Choice(name="#"+str(i),value=i)for i in poss[:8]]
    elif curgen == 3:
        allnums = range(1,15000)
        poss = [num for num in allnums if str(num).startswith(current)]
        return [Choice(name="#"+str(i),value=i)for i in poss[:8]]
    else:
        return [Choice(name="Invalid generation",value="Invalid generation")]
