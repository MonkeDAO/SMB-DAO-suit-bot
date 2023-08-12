from PIL import Image, ImageSequence
import discord
import asyncio
from io import BytesIO
from discord.components import SelectOption
from discord.enums import ButtonStyle
import os
from math import ceil
import functools

async def load_asset(guild: discord.Guild, path : str, oldimg : Image = None) -> tuple[list[SelectOption], dict]:
    options = []
    imgdict = {}
    if path == "pfp_backgrounds":
        common = await common_color(oldimg)
        options.append(SelectOption(label="None",value="none"))
        imgdict["default"] = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", oldimg.size, common)
        imgdict["none"] = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", oldimg.size, (0,0,0,0))
    elif path == "wallpapers" or path == "watchfaces" or path == "banners":
        pass
    else:
        imgdict["default"] = None
    for item in os.listdir("assets/" + path):
        if item == ".DS_Store":
            continue
        option = SelectOption(label=item[:-4],value=item[:-4].replace(" ","").lower())
        for emoji in guild.emojis:
            print(emoji.name)
            if emoji.name == item[:-4].replace(" ",""):
                option.emoji = emoji
                if path == "banners" and item[:-4].replace(" ","").lower() in ["black","green","blue","greenbananas","bluebananas","whitebananas"]:
                    continue
                break
        options.append(option)
        imgdict[item[:-4].replace(" ","").lower()] = await asyncio.get_event_loop().run_in_executor(None, Image.open, "assets/" + path + "/" + item)
    return options, imgdict
 
async def common_color(img: Image) -> tuple:
    pixels = await asyncio.get_event_loop().run_in_executor(None, img.getcolors)
    most_common = max(pixels, key=lambda x: x[0])
    return most_common[1]

class ImageView(discord.ui.View):
    def __init__(self, image : Image, interaction : discord.Interaction):
        self.image = image
        self.pastinteraction = interaction
        self.orgsize = image.size
        self.sizemultiplier = 1
        self.extension = "png"
        super().__init__(timeout=None)
    
    @discord.ui.button(label="PNG", style=ButtonStyle.green)
    async def png(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.image = await asyncio.get_event_loop().run_in_executor(None, self.image.convert, "RGBA")
        imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.image.save, imgbytes, "PNG")
        imgbytes.seek(0)
        file = discord.File(imgbytes, filename="monke.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://monke.png")
        self.extension = "png"
        await self.pastinteraction.followup.edit_message(self.pastinteraction.message.id, attachments=[file], embed=embed)
    
    @discord.ui.button(label="JPEG", style=ButtonStyle.green)
    async def jpeg(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.image = await asyncio.get_event_loop().run_in_executor(None, self.image.convert, "RGB")
        imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.image.save, imgbytes, "JPEG")
        imgbytes.seek(0)
        file = discord.File(imgbytes, filename="monke.jpeg")
        embed = discord.Embed()
        embed.set_image(url="attachment://monke.jpeg")
        self.extension = "jpeg"
        await self.pastinteraction.followup.edit_message(self.pastinteraction.message.id, attachments=[file], embed=embed)
    
    @discord.ui.button(label="WEBP", style=ButtonStyle.green)
    async def webp(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        self.image = await asyncio.get_event_loop().run_in_executor(None, self.image.convert, "RGBA")
        imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.image.save, imgbytes, "WEBP")
        imgbytes.seek(0)
        file = discord.File(imgbytes, filename="monke.webp")
        embed = discord.Embed()
        embed.set_image(url="attachment://monke.webp")
        self.extension = "webp"
        await self.pastinteraction.followup.edit_message(self.pastinteraction.message.id, attachments=[file], embed=embed)

class SelectReturn(discord.ui.Select):
    def __init__(self, options: list[SelectOption], imgdict: dict, placeholder: str, type: str):
        self.imgdict = imgdict
        self.traittype = type
        options.sort(key=lambda x: x.label)
        options.insert(0, SelectOption(label="Default",value="default"))
        if len(options) > 25:
            self.optionslist = []
            for i in range(ceil(len(options) / 23)):
                self.optionslist.append([])
                self.optionslist[i].append(SelectOption(label=f"Next Page", value=f"newpage{i+1}"))
                self.optionslist[i].append(SelectOption(label=f"Last Page", value=f"newpage{i-1}"))
                self.optionslist[i].extend(options[i*23:(i+1)*23])
        else:
            self.optionslist = [options[:25]]
        super().__init__(options=self.optionslist[0], placeholder=placeholder)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.traittype == "wallpaper" or self.traittype == "watchface":
            bg = self.imgdict[self.values[0]]
            if not self.view.transparent:
                newpixels = []
                result = await common_color(self.view.img)
                pixels = await asyncio.get_event_loop().run_in_executor(None, self.view.img.getdata)
                for pixel in pixels:
                    if (pixel == result) or (abs(result[0] - pixel[0]) <= 5 and abs(result[1] - pixel[1]) <= 5 and abs(result[2] - pixel[2]) <= 5):
                        newpixels.append((0,0,0,0))
                    else:
                        newpixels.append(pixel)
                self.view.transparent = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", self.view.img.size, (0,0,0,0))
                await asyncio.get_event_loop().run_in_executor(None, self.view.transparent.putdata, newpixels)
            baseimage = self.view.transparent
            if self.view.traits["outfit"]:
                if self.view.traits["outfit"].size != self.view.img.size:
                    self.view.traits["outfit"] = await asyncio.get_event_loop().run_in_executor(None, self.view.traits["outfit"].resize, self.view.img.size)
                baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, baseimage, self.view.traits['outfit'])
            if self.view.traits["sombrero"]:
                if self.view.traits["sombrero"].size != self.view.img.size:
                    self.view.traits["sombrero"] = await asyncio.get_event_loop().run_in_executor(None, self.view.traits["sombrero"].resize, self.view.img.size)
                baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, baseimage, self.view.traits['sombrero'])
            if self.traittype == "wallpaper":
                monke = await asyncio.get_event_loop().run_in_executor(None, baseimage.resize, (baseimage.width*5, baseimage.height*5))
                await asyncio.get_event_loop().run_in_executor(None, bg.paste, monke, (0,1920), monke)
            else:
                monke = await asyncio.get_event_loop().run_in_executor(None, baseimage.resize, (int(baseimage.width*2.3), int(baseimage.height*2.3)))
                await asyncio.get_event_loop().run_in_executor(None, bg.paste, monke, (-40,85), monke)
            self.view.img = bg
            self.view.imgbytes = BytesIO()
            await asyncio.get_event_loop().run_in_executor(None, self.view.img.save, self.view.imgbytes, "PNG")
            self.view.imgbytes.seek(0)
            file = discord.File(self.view.imgbytes, filename="monke.png")
            self.view.embed.set_image(url="attachment://monke.png")
            await interaction.followup.edit_message(message_id=self.view.msgid, embed=self.view.embed, view=ImageView(bg, interaction), attachments=[file])
        else:
            if self.values[0].startswith("newpage"):
                page = int(self.values[0][-1])
                if page > len(self.optionslist) - 1:
                    page = 0
                if page < 0:
                    page = len(self.optionslist) - 1
                self.options = self.optionslist[page]
                self.view.clear_items()
                self.view.add_item(self) 
                await interaction.followup.edit_message(message_id=self.view.msgid, view=self.view)
            else:
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
        self.imgtype = "png"
        self.traits = {"background":"default", "outfit":None, "sombrero":None, "gif":None}
        super().__init__(timeout=None)
    
    async def update_img(self, interaction : discord.Interaction):
        if not self.transparent:
            newpixels = []
            result = await common_color(self.img)
            pixels = await asyncio.get_event_loop().run_in_executor(None, self.img.getdata)
            for pixel in pixels:
                if (pixel == result) or (abs(result[0] - pixel[0]) <= 5 and abs(result[1] - pixel[1]) <= 5 and abs(result[2] - pixel[2]) <= 5):
                    newpixels.append((0,0,0,0))
                else:
                    newpixels.append(pixel)
            self.transparent = await asyncio.get_event_loop().run_in_executor(None, Image.new, "RGBA", self.img.size, (0,0,0,0))
            await asyncio.get_event_loop().run_in_executor(None, self.transparent.putdata, newpixels)
        if self.traits["background"] == "default" or self.traits["gif"]:
            try:
                backgroundimg = self.backgrounddict["default"]
            except:
                background_options, self.backgrounddict = await load_asset(self.emoji_guild, "pfp_backgrounds", self.orgimg)
                backgroundimg = self.backgrounddict["default"]
        else:
            backgroundimg = self.traits["background"]
        baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, backgroundimg, self.transparent)
        if self.traits["outfit"]:
            if self.traits["outfit"].size != self.img.size:
                self.traits["outfit"] = await asyncio.get_event_loop().run_in_executor(None, self.traits["outfit"].resize, self.img.size)
            baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, baseimage, self.traits['outfit'])
        if self.traits["sombrero"]:
            if self.traits["sombrero"].size != self.img.size:
                self.traits["sombrero"] = await asyncio.get_event_loop().run_in_executor(None, self.traits["sombrero"].resize, self.img.size)
            baseimage = await asyncio.get_event_loop().run_in_executor(None, Image.alpha_composite, baseimage, self.traits['sombrero'])
        if self.traits["gif"]:
            self.imgtype = "gif"
            animated_gif = self.traits["gif"]
            frames = []
            for f in ImageSequence.Iterator(animated_gif):
                frame = await asyncio.get_event_loop().run_in_executor(None, f.convert, "RGBA")
                monke = baseimage.copy()
                await asyncio.get_event_loop().run_in_executor(None, monke.paste, frame, (0,0), frame)
                frames.append(monke)
            baseimage = frames
        else:
            self.imgtype = "png"
        if self.imgtype == "png":
            self.img = baseimage
            self.imgbytes = BytesIO()
            await asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
            self.imgbytes.seek(0)
            file = discord.File(self.imgbytes, filename="monke.png")
            self.embed.set_image(url="attachment://monke.png")
        else:
            self.imgbytes = BytesIO()
            if animated_gif == self.gifdict["welcome"]:
                await asyncio.get_event_loop().run_in_executor(None, functools.partial(baseimage[0].save, self.imgbytes, "GIF", save_all=True, append_images=baseimage[1:], duration=500, loop=0))
            else:
                await asyncio.get_event_loop().run_in_executor(None, functools.partial(baseimage[0].save, self.imgbytes, "GIF", save_all=True, append_images=baseimage[1:], loop=0))
            self.imgbytes.seek(0)
            file = discord.File(self.imgbytes, filename="monkegif.gif")
            self.embed.set_image(url="attachment://monkegif.gif")
        self.clear_items()
        self.add_item(self.pick_background)
        self.add_item(self.pick_outfit)
        self.add_item(self.pick_sombrero)
        self.add_item(self.pick_gif)
        self.add_item(self.save_wallpaper)
        self.add_item(self.save_watchface)
        await interaction.followup.edit_message(self.msgid, embed=self.embed, attachments=[file], view=self)
    
    @discord.ui.button(label="Background", style=ButtonStyle.green)
    async def pick_background(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        background_options, self.backgrounddict = await load_asset(self.emoji_guild,"pfp_backgrounds", self.orgimg)
        self.add_item(SelectReturn(background_options, placeholder="Pick a background", imgdict=self.backgrounddict, type="background"))
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Outfit", style=ButtonStyle.green)
    async def pick_outfit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        outfit_options, self.outfitdict = await load_asset(self.emoji_guild, "outfits")
        self.add_item(SelectReturn(outfit_options, placeholder="Pick an outfit", imgdict=self.outfitdict, type="outfit"))
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Sombrero", style=ButtonStyle.green)
    async def pick_sombrero(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        sombrero_options, self.sombrerodict = await load_asset(self.emoji_guild, "sombreros")
        self.add_item(SelectReturn(sombrero_options, placeholder="Pick a sombrero", imgdict=self.sombrerodict, type="sombrero"))
        await interaction.response.edit_message(view=self)
        
    @discord.ui.button(label="Gif", style=ButtonStyle.green)
    async def pick_gif(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        gif_options, self.gifdict = await load_asset(self.emoji_guild, "gifs")
        self.add_item(SelectReturn(gif_options, placeholder="Pick a gif", imgdict=self.gifdict, type="gif"))
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Save As Wallpaper", style=ButtonStyle.green)
    async def save_wallpaper(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        wallpaper_options, self.wallpaperdict = await load_asset(self.emoji_guild, "wallpapers")
        self.add_item(SelectReturn(wallpaper_options, placeholder="Pick a wallpaper", imgdict=self.wallpaperdict, type="wallpaper"))
        await interaction.response.edit_message(view=self)
    
    @discord.ui.button(label="Save As Watch Face", style=ButtonStyle.green)
    async def save_watchface(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        watchface_options, self.watchfacedict = await load_asset(self.emoji_guild, "watchfaces")
        self.add_item(SelectReturn(watchface_options, placeholder="Pick a watch face", imgdict=self.watchfacedict, type="watchface"))
        await interaction.response.edit_message(view=self)

class DressUpViewGen3(discord.ui.View):
    def __init__(self, monke : dict, image : Image, id : int, embed : discord.Embed, EmojiGuild : discord.Guild):
        self.monke = monke
        self.img = image
        self.imgbytes : BytesIO = BytesIO()
        asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
        self.imgbytes.seek(0)
        self.orgimg = Image.frombytes(image.mode, image.size, image.tobytes())
        self.msgid = id
        self.embed = embed
        self.emoji_guild = EmojiGuild
        self.imgtype = "png"
        self.traits = {"gif":None}
        super().__init__(timeout=None)
    
    async def update_img(self, interaction : discord.Interaction):
        if self.traits["gif"]:
            self.imgtype = "gif"
            animated_gif = self.traits["gif"]
            frames = []
            for f in ImageSequence.Iterator(animated_gif):
                frame = await asyncio.get_event_loop().run_in_executor(None, f.convert, "RGBA")
                monke = self.orgimg.copy()
                await asyncio.get_event_loop().run_in_executor(None, monke.paste, frame, (0,0), frame)
                frames.append(monke)
            baseimage = frames
        else:
            self.imgtype = "png"
        if self.imgtype == "png":
            self.img = baseimage
            self.imgbytes = BytesIO()
            await asyncio.get_event_loop().run_in_executor(None, self.img.save, self.imgbytes, "PNG")
            self.imgbytes.seek(0)
            file = discord.File(self.imgbytes, filename="monke.png")
            self.embed.set_image(url="attachment://monke.png")
        else:
            self.imgbytes = BytesIO()
            if animated_gif == self.gifdict["welcome"]:
                await asyncio.get_event_loop().run_in_executor(None, functools.partial(baseimage[0].save, self.imgbytes, "GIF", save_all=True, append_images=baseimage[1:], duration=500, loop=0))
            else:
                await asyncio.get_event_loop().run_in_executor(None, functools.partial(baseimage[0].save, self.imgbytes, "GIF", save_all=True, append_images=baseimage[1:], loop=0))
            self.imgbytes.seek(0)
            file = discord.File(self.imgbytes, filename="monkegif.gif")
            self.embed.set_image(url="attachment://monkegif.gif")
        self.clear_items()
        self.add_item(self.pick_gif)
        await interaction.followup.edit_message(self.msgid, embed=self.embed, attachments=[file], view=self)
        
    @discord.ui.button(label="Gif", style=ButtonStyle.green)
    async def pick_gif(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.clear_items()
        gif_options, self.gifdict = await load_asset(self.emoji_guild, "gifs")
        self.add_item(SelectReturn(gif_options, placeholder="Pick a gif", imgdict=self.gifdict, type="gif"))
        await interaction.response.edit_message(view=self)

class BannerSelect(discord.ui.Select):
    def __init__(self,options):
        super().__init__(placeholder="Pick your banner!", options=options)
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        self.view.remove_item(self)
        self.view.add_item(BannerSelect(self.options))
        self.view.banner = self.view.bannerdict[interaction.data["values"][0]]
        await self.view.change_banner(interaction)

class BannerView(discord.ui.View):
    def __init__(self, monkes: [Image], banner : Image, bannerdict : dict, msg : discord.Message):
        self.monkes = monkes
        self.banner = banner
        self.bannerdict = bannerdict
        self.orgsize = 384
        self.msgid = msg.id
        super().__init__(timeout=None)
    
    async def change_banner(self, interaction: discord.Interaction):
        bg = self.banner.copy()
        banner_name = [k for k, v in self.bannerdict.items() if v == self.banner][0]
        for monke in self.monkes:
            if monke.size != (self.orgsize,self.orgsize):
                monke = await asyncio.get_event_loop().run_in_executor(None, monke.resize, (int(self.orgsize*1.5),int(self.orgsize*1.5)))
        if banner_name == "Yellow Blue" or banner_name == "Blue Green Wave":
            self.monkes[0] = await asyncio.get_event_loop().run_in_executor(None, self.monkes[0].resize, (int(self.orgsize*2.60416666667),int(self.orgsize*2.60416666667)))
        for i, v in enumerate(self.monkes):
            if banner_name == "Yellow Blue" or banner_name == "Blue Green Wave":
                if i == 0:
                    await asyncio.get_event_loop().run_in_executor(None, bg.paste, v, (2040, 0), v)
                else:
                    await asyncio.get_event_loop().run_in_executor(None, bg.paste, v, (1500-((i-1)*400), 424), v)
            elif banner_name == "Black" or banner_name == "Blue" or banner_name == "Green":
                await asyncio.get_event_loop().run_in_executor(None, bg.paste, v, (1500-(i*400), 424), v)
            else:
                await asyncio.get_event_loop().run_in_executor(None, bg.paste, v, (2000-(i*400), 424), v)
        imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, bg.save, imgbytes, "PNG")
        imgbytes.seek(0)
        file = discord.File(imgbytes, filename="monke.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://monke.png")
        self.banner = bg
        await interaction.followup.edit_message(message_id=self.msgid,embed=embed, attachments=[file], view=self)
    
    @discord.ui.button(label="Save", style=ButtonStyle.green, row=1)
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        imgbytes = BytesIO()
        await asyncio.get_event_loop().run_in_executor(None, self.banner.save, imgbytes, "PNG")
        imgbytes.seek(0)
        file = discord.File(imgbytes, filename="monke.png")
        embed = discord.Embed()
        embed.set_image(url="attachment://monke.png")
        await interaction.response.edit_message(embed=embed, view=ImageView(self.banner, interaction), attachments=[file])
        

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
        
    
    