from PIL import Image
import discord
import asyncio
from io import BytesIO
from discord.enums import ButtonStyle

async def common_color(img: Image) -> tuple:
    pixels = await asyncio.get_event_loop().run_in_executor(None, img.getcolors)
    most_common = max(pixels, key=lambda x: x[0])
    return most_common[1]

class DressUpViewGen2(discord.ui.View):
    def __init__(self, monke : dict, image : Image, id : int):
        self.monke = monke
        self.img  = image
        self.id = id
        super().__init__(timeout=None)
    
    async def display_new(self, img : Image):
        pass
    
    @discord.ui.button(label="Remove Background", style=ButtonStyle.green)
    async def remove_background(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        result = await common_color(self.img)
        pixels = await asyncio.get_event_loop().run_in_executor(None, self.img.getdata)
        newpixels = []
        for pixel in pixels:
            if pixel == result:
                newpixels.append((0,0,0,0))
            else:
                newpixels.append(pixel)
        self.img.putdata(newpixels)

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
        
    
    