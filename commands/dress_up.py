import sys
sys.path.append('..')
import discord
from discord.app_commands import Choice
from views.edit_views import DressUpViewGen2
from config import bot, gen2List, gen3List
from PIL import Image
import asyncio
from io import BytesIO
import os
import aiohttp

@bot.tree.command(name="dress-up", description="Dress up your monke!")
async def dressup(interaction: discord.Interaction, generation: int, monke: int):
    await interaction.response.defer(ephemeral=True)
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
        view = DressUpViewGen2(monke, img, msg.id)
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

""" Deprecated
@bot.tree.command(name="make-your-monke", description="Create your own monke!")
async def dressup(interaction: discord.Interaction, generation: int, template: int = None):
    await interaction.response.defer(ephemeral=True)
    emoji_guild = bot.get_guild(1101931928409612411)
    if template == "Invalid generation" or template == None: template = {}
    if (generation != 2 and generation != 3):
        await interaction.followup.send("Invalid generation", ephemeral=True)
        return
    if generation == 2:
        traits = {}
        if template != {}:
            for i in gen2List:
                if int(i['mint']["name"].split("#")[1]) == template:
                    template = {}
                    for trait in i['mint']['attributes']:
                        template[trait['trait_type']] = trait['value']
                    break
            if type(template) == int:
                await interaction.followup.send("The monke you tried to use for the template could not be found", ephemeral=True)
                template = {}
        if generation == 2:
            path = "art"
        traits = os.listdir(path)
        traits.remove(".DS_Store")
        traitdict = {}
        for trait in traits:
            if trait != "Type":
                traitdict[trait] = {"None":None}
            else:
                traitdict[trait] = {}
            options = os.listdir(path + "/" + trait)
            try:
                options.remove(".DS_Store")
            except:
                pass
            for option in options:
                img = await asyncio.get_event_loop().run_in_executor(None, Image.open, path + "/" + trait + "/" + option)
                traitdict[trait][option[:-4]] = img
        selected_traits = {}
        for k, v in template.items():
            if k in traitdict.keys():
                if v == "None":
                    selected_traits[k] = None
                else:
                    try:
                        selected_traits[k] = traitdict[k][v]
                    except:
                        selected_traits[k] = None
        for k, v in traitdict.items():
            if template == {}:
                if k != "Type":
                    if k not in selected_traits.keys():
                        selected_traits[k] = None
                if k == "Type":
                    if k not in selected_traits.keys():
                        selected_traits[k] = v["Solana"]
        img = await generate_image(selected_traits)
        bytes = BytesIO()
        img.save(bytes, format="PNG")
        bytes.seek(0)
        file = discord.File(bytes, filename="template.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://template.png")
        msg = await interaction.followup.send(embed=embed, file=file)
        traitdict = {"Type":traitdict["Type"], "Clothes":traitdict["Clothes"], "Ears":traitdict["Ears"], "Eyes":traitdict["Eyes"], "Mouth":traitdict["Mouth"]}
        view = DressUpView(generation, embed, selected_traits, traitdict, emoji_guild)
        for k,v in traitdict.items():
            view.add_item(BaseButton(k, v, view, msg.id))
        await msg.edit(view=view)
        
@dressup.autocomplete("generation")
async def genauto(interaction: discord.Interaction, current: str):
    return [Choice(name="Gen 2", value="2"), Choice(name="Gen 3", value="3")]

@dressup.autocomplete("template")
async def templateauto(interaction: discord.Interaction, current: str):
    curgen = interaction.namespace.generation
    if curgen == 2:
        allnums = range(1,5000)
        poss = [num for num in allnums if str(num).startswith(current)]
        return [Choice(name="#"+str(i),value=i)for i in poss[:8]]
    elif curgen == 3:
        return [Choice(name="#"+str(i),value=i)for i in range(1,15000)]
    else:
        return [Choice(name="Invalid generation",value="Invalid generation")]
"""