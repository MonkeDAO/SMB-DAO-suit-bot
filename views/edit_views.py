from PIL import Image
import discord
import asyncio
from io import BytesIO
from discord.components import SelectOption
from discord.enums import ButtonStyle
import os
    
async def load_asset(guild: discord.Guild, oldimg : Image, path : str) -> tuple[list[SelectOption], dict]:
    background_options = [SelectOption(label="Default",value="default")]
    imgdict = {}
    if path == "pfp_backgrounds":
        common = await common_color(oldimg)
        background_options.append(SelectOption(label="None",value="none"))
        imgdict["default"] = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", oldimg.size, common)
        imgdict["none"] = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", oldimg.size, (0,0,0,0))
    else:
        imgdict["default"] = None
    for item in os.listdir("assets/" + path):
        if item == ".DS_Store":
            continue
        option = SelectOption(label=item[:-4],value=item[:-4].replace(" ","").lower())
        for emoji in guild.emojis:
            if emoji.name == item[:-4].replace(" ",""):
                option.emoji = emoji
                break
        background_options.append(option)
        imgdict[item[:-4].replace(" ","").lower()] = await asyncio.get_event_loop().run_in_executor(None, Image.open, "assets/" + path + "/" + item)
    return background_options, imgdict
 
async def common_color(img: Image) -> tuple:
    pixels = await asyncio.get_event_loop().run_in_executor(None, img.getcolors)
    most_common = max(pixels, key=lambda x: x[0])
    return most_common[1]

class SelectReturn(discord.ui.Select):
    def __init__(self, options: list[SelectOption], imgdict: dict, placeholder: str, type: str):
        self.imgdict = imgdict
        self.traittype = type
        super().__init__(options=options, placeholder=placeholder)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        self.view.traits[self.traittype] = self.imgdict[self.values[0]]
        await self.view.update_img(interaction)

class DressUpViewGen2(discord.ui.View):
    def __init__(self, monke : dict, image : Image, id : int, embed : discord.Embed, EmojiGuild : discord.Guild):
        self.monke = monke
        self.img = image
        self.imgbytes : BytesIO = BytesIO()
        asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
        self.imgbytes.seek(0)
        self.orgimg = Image.frombytes(image.mode, image.size, image.tobytes())
        self.transparent = None
        self.msgid = id
        self.embed = embed
        self.emoji_guild = EmojiGuild
        self.traits = {"background":"default", "outfit":None}
        super().__init__(timeout=None)
    
    async def update_img(self, interaction : discord.Interaction):
        if not self.transparent:
            newpixels = []
            result = await common_color(self.img)
            pixels = await asyncio.get_event_loop().run_in_executor(None, self.img.getdata)
            for pixel in pixels:
                if pixel == result:
                    newpixels.append((0,0,0,0))
                else:
                    newpixels.append(pixel)
            self.transparent = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", self.img.size, (0,0,0,0))
            await asyncio.get_event_loop().run_in_executor(None, self.transparent.putdata, newpixels)
        if self.traits["background"] == "default":
            try:
                backgroundimg = self.backgrounddict["default"]
            except:
                background_options, self.backgrounddict = await load_asset(self.emoji_guild, self.orgimg, "pfp_backgrounds")
                backgroundimg = self.backgrounddict["default"]
        else:
            backgroundimg = self.traits["background"]
        baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, backgroundimg, self.transparent)
        if self.traits["outfit"]:
            if self.traits["outfit"].size != self.img.size:
                self.traits["outfit"] = await asyncio.get_event_loop().run_in_executor(None, self.traits["outfit"].resize, self.img.size)
            baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, baseimage, self.traits['outfit'])
        self.img = baseimage
        self.imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
        self.imgbytes.seek(0)
        file = discord.File(self.imgbytes, filename="monke.png")
        self.embed.set_image(url="attachment://monke.png")
        self.clear_items()
        self.add_item(self.pick_background)
        self.add_item(self.pick_outfit)
        await interaction.followup.edit_message(self.msgid, embed=self.embed, attachments=[file], view=self)
    
    @discord.ui.button(label="Background", style=ButtonStyle.green)
    async def pick_background(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        background_options, self.backgrounddict = await load_asset(self.emoji_guild, self.orgimg, "pfp_backgrounds")
        self.add_item(SelectReturn(background_options, placeholder="Pick a background", imgdict=self.backgrounddict, type="background"))
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Outfit", style=ButtonStyle.green)
    async def pick_outfit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        outfit_options, self.outfitdict = await load_asset(self.emoji_guild, self.orgimg, "outfits")
        self.add_item(SelectReturn(outfit_options, placeholder="Pick an outfit", imgdict=self.outfitdict, type="outfit"))
        await interaction.response.edit_message(view=self)

""" Deprecated
async def generate_image(traits: dict) -> Image:
    image = traits["Type"]
    sortedtraits = {"Type":traits["Type"], "Clothes":traits["Clothes"], "Ears":traits["Ears"], "Eyes":traits["Eyes"], "Mouth":traits["Mouth"]}
    for k, v in sortedtraits.items():
        if v == None:
            continue
        else:
            image = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, image, v)
    return image
    
class BaseSelect(discord.ui.Select):
    def __init__(self, name: str, traits: dict, view : discord.ui.View, id : int):
        options = []
        for trait in traits.keys():
            try:
                emoji = [em for em in view.emoji_guild.emojis if em.name == trait.replace(" ","")][0]
            except:
                emoji = None
            options.append(discord.SelectOption(label=trait,value=trait,emoji=emoji))
        self.name = name
        self.lastview = view
        self.msgid = id
        super().__init__(placeholder="Pick a trait", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        selected = self.values[0]
        self.lastview.selected_traits[self.name] = self.lastview.traitdict[self.name][selected]
        img = await generate_image(self.lastview.selected_traits)
        embed = self.lastview.embed
        bytes = BytesIO()
        img.save(bytes, format="PNG")
        bytes.seek(0)
        file = discord.File(bytes, filename="monke.png")
        embed.set_image(url="attachment://monke.png")
        await interaction.followup.edit_message(self.msgid, embed=embed, attachments=[file], view=self.lastview)

class BaseButton(discord.ui.Button):
    def __init__(self, name: str, traits: dict, view : discord.ui.View, id : int):
        self.name = name
        self.traits = traits
        self.lastview = view
        self.msgid = id
        super().__init__(style=ButtonStyle.green, label=name)
    
    async def callback(self, interaction: discord.Interaction):
        selectview = discord.ui.View().add_item(BaseSelect(self.name,self.traits,self.lastview,self.msgid))
        await interaction.response.edit_message(view=selectview)

class DressUpView(discord.ui.View):
    def __init__(self, gen: int, embed: discord.Embed, template: dict, traitdict: dict, emoji_guild: discord.Guild):
        super().__init__(timeout=None)
        self.embed = embed
        self.traitdict = traitdict
        self.selected_traits = template
        self.emoji_guild = emoji_guild
"""
        
    
    