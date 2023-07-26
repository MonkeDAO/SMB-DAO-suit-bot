from PIL import Image
import discord
import asyncio
from io import BytesIO
from discord.components import SelectOption
from discord.enums import ButtonStyle
import os
    
async def load_backgrounds(guild: discord.Guild, oldimg : Image) -> tuple[list[SelectOption], dict]:
    background_options = [SelectOption(label="Default",value="default"), SelectOption(label="None",value="none")]
    imgdict = {}
    common = await common_color(oldimg)
    imgdict["default"] = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", oldimg.size, common)
    imgdict["none"] = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", oldimg.size, (0,0,0,0))
    for bg in os.listdir("assets/pfp_backgrounds"):
        if bg == ".DS_Store":
            continue
        option = SelectOption(label=bg[:-4],value=bg[:-4].replace(" ","").lower())
        for emoji in guild.emojis:
            if emoji.name == bg[:-4].replace(" ",""):
                option.emoji = emoji
                break
        background_options.append(option)
        imgdict[bg[:-4].replace(" ","").lower()] = await asyncio.get_event_loop().run_in_executor(None, Image.open, "assets/pfp_backgrounds/" + bg)
    return background_options, imgdict
 
async def common_color(img: Image) -> tuple:
    pixels = await asyncio.get_event_loop().run_in_executor(None, img.getcolors)
    most_common = max(pixels, key=lambda x: x[0])
    return most_common[1]

class SelectReturn(discord.ui.Select):
    def __init__(self, options: list[SelectOption], imgdict: dict, placeholder: str = None):
        self.imgdict = imgdict
        super().__init__(options=options, placeholder=placeholder)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await self.view.set_background(self.imgdict[self.values[0]], interaction)

class DressUpViewGen2(discord.ui.View):
    def __init__(self, monke : dict, image : Image, id : int, embed : discord.Embed, EmojiGuild : discord.Guild):
        self.monke = monke
        self.img = image
        self.imgbytes : BytesIO = BytesIO()
        asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
        self.imgbytes.seek(0)
        self.orgimg = Image.frombytes(image.mode, image.size, image.tobytes())
        self.msgid = id
        self.embed = embed
        super().__init__(timeout=None)
    
    async def set_background(self, img : Image, interaction : discord.Interaction):
        newpixels = []
        result = await common_color(self.orgimg)
        pixels = await asyncio.get_event_loop().run_in_executor(None, self.orgimg.getdata)
        for pixel in pixels:
            if pixel == result:
                newpixels.append((0,0,0,0))
            else:
                newpixels.append(pixel)
        blankimg = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", self.orgimg.size, (0,0,0,0))
        await asyncio.get_event_loop().run_in_executor(None, blankimg.putdata, newpixels)
        self.img = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, img, blankimg)
        self.imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
        self.imgbytes.seek(0)
        file = discord.File(self.imgbytes, filename="monke.png")
        self.embed.set_image(url="attachment://monke.png")
        self.clear_items()
        self.add_item(self.pick_background)
        await interaction.followup.edit_message(self.msgid, embed=self.embed, attachments=[file], view=self)
    
    @discord.ui.button(label="Background", style=ButtonStyle.green)
    async def pick_background(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        background_options, self.backgrounddict = await load_backgrounds(interaction.guild, self.orgimg)
        self.add_item(SelectReturn(background_options, placeholder="Pick a background", imgdict=self.backgrounddict))
        await interaction.response.edit_message(view=self)
        """
        newpixels = []
        if self.background:
            result = await common_color(self.img)
            pixels = await asyncio.get_event_loop().run_in_executor(None, self.img.getdata)
            for pixel in pixels:
                if pixel == result:
                    newpixels.append((0,0,0,0))
                else:
                    newpixels.append(pixel)
            self.background = False
        else:
            result = await common_color(self.orgimg)
            pixels = await asyncio.get_event_loop().run_in_executor(None, self.img.getdata)
            for pixel in pixels:
                if pixel == (0,0,0,0):
                    newpixels.append(result)
                else:
                    newpixels.append(pixel)
            self.background = True
        await asyncio.get_event_loop().run_in_executor(None, self.img.putdata, newpixels)
        self.imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
        self.imgbytes.seek(0)
        file = discord.File(self.imgbytes, filename="monke.png")
        self.embed.set_image(url="attachment://monke.png")
        await interaction.followup.edit_message(self.msgid, embed=self.embed, attachments=[file], view=self)
        """
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
        
    
    