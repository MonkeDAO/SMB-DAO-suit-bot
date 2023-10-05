import discord
from config import bot, gen2List
from discord.app_commands import Choice
import aiohttp
from PIL import Image
import asyncio
from io import BytesIO
from views.edit_views import load_asset, common_color, BannerView, BannerSelect

@bot.tree.command(name="banner", description="Create a banner!")
async def banner(interaction: discord.Interaction, monke1 : int = None, monke2 : int = None, monke3 : int = None, monke4 : int = None, monke5 : int = None):
    await interaction.response.defer(ephemeral=True)
    monkedict = {monke1: None, monke2: None, monke3: None, monke4: None, monke5: None}
    try:
        del monkedict[None]
    except:
        pass
    emoji_guild = bot.get_guild(1101931928409612411)
    for i in gen2List:
        for monke in monkedict:
            if int(i['mint']["name"].split("#")[1]) == monke:
                async with aiohttp.ClientSession() as session:
                    async with session.get(i['mint']['imageUri']) as resp:
                        img = await resp.read()
                        img = await asyncio.get_event_loop().run_in_executor(None, Image.open, BytesIO(img))
                        newpixels = []
                        result = await common_color(img)
                        pixels = await asyncio.get_event_loop().run_in_executor(None, img.getdata)
                        for pixel in pixels:
                            if (pixel == result) or (abs(result[0] - pixel[0]) <= 5 and abs(result[1] - pixel[1]) <= 5 and abs(result[2] - pixel[2]) <= 5):
                                newpixels.append((0,0,0,0))
                            else:
                                newpixels.append(pixel)
                        transparent = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", img.size, (0,0,0,0))
                        await asyncio.get_event_loop().run_in_executor(None, transparent.putdata, newpixels)
                        img = await asyncio.get_event_loop().run_in_executor(None, transparent.resize, (int(img.width*1.5), int(img.height*1.5)))
                        monkedict[monke] = img
    monkedict = {k: v for k, v in monkedict.items() if v is not None}
    options, bannerdict = await load_asset(emoji_guild, "banners")
    default = bannerdict["black"]
    for i, v in enumerate(monkedict.values()):
        await asyncio.get_event_loop().run_in_executor(None, default.paste, v, (1500-(i*400), 424), v)
    imgbytes = BytesIO()
    await asyncio.get_event_loop().run_in_executor(None, default.save, imgbytes, "PNG")
    imgbytes.seek(0)
    file = discord.File(imgbytes, filename="monke.png")
    embed = discord.Embed()
    embed.set_image(url="attachment://monke.png")
    msg = await interaction.followup.send(file=file, embed=embed, ephemeral=True)
    view = BannerView(list(monkedict.values()), bannerdict["black"], bannerdict, msg)
    view.add_item(BannerSelect(options))
    await msg.edit(view=view)

@banner.autocomplete("monke1")
async def monke1auto(interaction: discord.Interaction, current: str):
    allnums = range(1,5000)
    poss = [num for num in allnums if str(num).startswith(current)]
    return [Choice(name="#"+str(i),value=i)for i in poss[:8]]

@banner.autocomplete("monke2")
async def monke1auto(interaction: discord.Interaction, current: str):
    allnums = range(1,5000)
    poss = [num for num in allnums if str(num).startswith(current)]
    return [Choice(name="#"+str(i),value=i)for i in poss[:8]]

@banner.autocomplete("monke3")
async def monke1auto(interaction: discord.Interaction, current: str):
    allnums = range(1,5000)
    poss = [num for num in allnums if str(num).startswith(current)]
    return [Choice(name="#"+str(i),value=i)for i in poss[:8]]

@banner.autocomplete("monke4")
async def monke1auto(interaction: discord.Interaction, current: str):
    allnums = range(1,5000)
    poss = [num for num in allnums if str(num).startswith(current)]
    return [Choice(name="#"+str(i),value=i)for i in poss[:8]]

@banner.autocomplete("monke5")
async def monke1auto(interaction: discord.Interaction, current: str):
    allnums = range(1,5000)
    poss = [num for num in allnums if str(num).startswith(current)]
    return [Choice(name="#"+str(i),value=i)for i in poss[:8]]