import os
import io
import json
import requests
from PIL import Image, ImageSequence

# Opening JSON file with pfps. Add your open file and update it to match the name here
data = open('monkeList.json')

# Folder locations for clean pfps, completed pfps, and outfits

save_img_folder = 'dressed_pfps/'
pfp_folder = 'assets/clean_pfps/'
outfits_folder = 'assets/outfits/'
no_background_folder = 'assets/no_background/'
wc_folder = 'assets/wc_kits/'
sombrero_folder = 'assets/sombreros/'
wallpaper_folder = 'assets/wallpapers/'
pfp_background_folder = 'assets/pfp_backgrounds/'
banner_folder = 'assets/banners/'
gif_folder = 'assets/gifs/'
watch_folder = 'assets/watchfaces/'


# Returns JSON object as a dictionary
pfp_atts = json.load(data)

outfits = ["bandito_santa_full", "bandito_santa", "blue", "cape", "daovote", "elf", "ghost", "halo", "horns", "masters", "portugal",
           "portugalsolana", "pumpkin", "santa_hat", "santa", "shotta", "sombrero", "stronger", "suit-blk", "suit-pink", "vote", "votebrero", "vr"]

wc_kits = ["argentina", "australia", "belgium", "brazil", "canada", "costarica", "croatia", "england", "france",
           "germany", "italy", "mexico", "mexico+", "netherlands", "portugal", "serbia", "southkorea", "spain", "usa"]
# Search for the pfp id in the JSON dictionary and return the image URL associated with that id. You'll need to update the keys to match what's in your JSON delattr

sombreros = ["black", "blacktie", "cinco",
             "easter", "october", "pink", "solana"]

phone_backgrounds = ["all_black", "black_fade", "black_stack",  "blue_stack", "blue",
                     "green_icons", "green_md", "green_stack", "green", "white_blue_md", "white_icons", "yellow"]

pfp_backgrounds = ["blue", "green", "red"]

banners = ["black", "blue_bananas", "blue_green_wave", "blue", "green_bananas", "green_wave", "green_white",
           "green", "white_bananas", "white_green", "white", "wordmark_blue", "wordmark_green", "yellow_blue"]

gifs = ["gm", "gm2", "gn", "gn2", "welcome"]

watches = ["black_stack", "blue_bananas", "blue_stack", "blue", "green_bananas",
           "green_monke", "green_stack", "green", "white_bananas", "white"]


def get_pfp_img_url(id):
    for pfp in pfp_atts:
        if id == pfp['number']:
            return pfp['Image']


# Downloads the pfp from the image URL and saves it in a directory

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)

# Combines the pfp image with a transparent png of the attribute  and saves it to an output directory


def get_dressed(fit: str, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def make_wallpaper(wallpaper, pfp_id):
    background = Image.open(wallpaper_folder + wallpaper.lower() + '.png')
    monke = Image.open(no_background_folder + pfp_id + '.png')
    monke = monke.resize((int(monke.width*5), int(monke.height*5)))
    background.paste(monke, (0, 1920), mask=monke)
    background.save(save_img_folder + wallpaper.lower() + str(pfp_id) + '.png')

    return


def make_watch(bg, pfp_id):
    background = Image.open(watch_folder + bg.lower() + '.png')
    monke = Image.open(no_background_folder + str(pfp_id) + '.png')
    monke = monke.resize((int(monke.width*2.3), int(monke.height*2.3)))
    background.paste(monke, (-40, 85), mask=monke)
    background.save(save_img_folder + bg.lower() + str(pfp_id) + '.png')

    return


def deleteDressed(fit, pfp_id):
    os.remove(save_img_folder + fit.lower() + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')


def get_kit(fit, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(wc_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def get_brero(fit, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    brero = Image.open(sombrero_folder + fit.lower() + '.png')

    pfp.paste(brero, (0, 0), mask=brero)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def no_background_wc(fit, pfp_id):
    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    outfit = Image.open(wc_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def no_background_fit(fit, pfp_id):
    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit.lower() + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def brero_no_background(fit, pfp_id):
    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    outfit = Image.open(sombrero_folder + str(pfp_id) + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + fit.lower() + str(pfp_id) + '.png')

    return


def pfp_background(background, pfp_id: int):
    pfp = Image.open(pfp_background_folder + background.lower() + '.png')
    monke = Image.open(no_background_folder + str(pfp_id) + '.png')

    pfp.paste(monke, (0, 0), mask=monke)

    pfp.save(save_img_folder + background.lower() + str(pfp_id) + '.png')

    return


def high_quality(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    monke = pfp.resize((int(pfp.width*5), int(pfp.height*5)))
    monke.save(save_img_folder + 'hq' + str(pfp_id) + '.png')

    return


def make_smol(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    pfp_bg_color = pfp.convert('RGB')
    r, g, b = pfp_bg_color.getpixel((300, 300))
    smol_im = pfp.resize((int(pfp.width/3), int(pfp.height/3)))

    smol = Image.new('RGB', (384, 384), (r, g, b))
    smol.paste(smol_im, (128, 256), mask=smol_im)

    smol.save(save_img_folder + 'smol' + str(pfp_id) + '.png')

    return


def make_smoller(pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    pfp_bg_color = pfp.convert('RGB')
    r, g, b = pfp_bg_color.getpixel((300, 300))
    smol_im = pfp.resize((int(pfp.width/6), int(pfp.height/6)))

    smol = Image.new('RGB', (384, 384), (r, g, b))
    smol.paste(smol_im, (160, 320), mask=smol_im)

    smol.save(save_img_folder + 'smol' + str(pfp_id) + '.png')

    return


def make_banner(ban, pfp_id, pfp2=None, pfp3=None, pfp4=None, pfp5=None):
    banner_string = ban.lower()
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')
    background = Image.open(banner_folder + banner_string + '.png')

    if banner_string == "yellow_blue" or banner_string == "blue_green_wave":

        monke = Image.open(pfp_folder + str(pfp_id) + '.png')
        monke = monke.resize(
            (int(monke.width*2.60416666667), int(monke.height*2.60416666667)))
        if pfp2:
            m2 = Image.open(no_background_folder + str(pfp2) + '.png')
            m2 = m2.resize((int(m2.width*1.5), int(m2.height*1.5)))
            background.paste(m2, (1500, 424), mask=m2)
            background.save(save_img_folder + banner_string +

                            str(pfp_id) + '.png')

        if pfp3:
            m3 = Image.open(no_background_folder + str(pfp3) + '.png')
            m3 = m3.resize((int(m3.width*1.5), int(m3.height*1.5)))
            background.paste(m3, (1100, 424), mask=m3)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp4:
            m4 = Image.open(no_background_folder + str(pfp4) + '.png')
            m4 = m4.resize((int(m4.width*1.5), int(m4.height*1.5)))
            background.paste(m4, (700, 424), mask=m4)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        if pfp5:
            m5 = Image.open(no_background_folder + str(pfp5) + '.png')
            m5 = m5.resize((int(m5.width*1.5), int(m5.height*1.5)))
            background.paste(m5, (300, 424), mask=m5)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        background.paste(monke, (2040, 0), mask=monke)
        background.save(save_img_folder + banner_string + str(pfp_id) + '.png')

    elif banner_string == "black" or banner_string == "blue" or banner_string == "green":
        monke = Image.open(no_background_folder + pfp_id + '.png')
        monke = monke.resize((int(monke.width*1.5), int(monke.height*1.5)))

        if pfp2:
            m2 = Image.open(no_background_folder + str(pfp2) + '.png')
            m2 = m2.resize((int(m2.width*1.5), int(m2.height*1.5)))
            background.paste(m2, (1100, 424), mask=m2)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp3:
            m3 = Image.open(no_background_folder + str(pfp3) + '.png')
            m3 = m3.resize((int(m3.width*1.5), int(m3.height*1.5)))
            background.paste(m3, (700, 424), mask=m3)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        if pfp4:
            m4 = Image.open(no_background_folder + str(pfp4) + '.png')
            m4 = m4.resize((int(m4.width*1.5), int(m4.height*1.5)))
            background.paste(m4, (300, 424), mask=m4)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp5:
            m5 = Image.open(no_background_folder + str(pfp5) + '.png')
            m5 = m5.resize((int(m5.width*1.5), int(m5.height*1.5)))
            background.paste(m5, (-100, 424), mask=m5)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        background.paste(monke, (1500, 424), mask=monke)
        background.save(save_img_folder + banner_string + str(pfp_id) + '.png')

    else:

        monke = Image.open(no_background_folder + pfp_id + '.png')
        monke = monke.resize((int(monke.width*1.5), int(monke.height*1.5)))

        if pfp2:
            m2 = Image.open(no_background_folder + str(pfp2) + '.png')
            m2 = m2.resize((int(m2.width*1.5), int(m2.height*1.5)))
            background.paste(m2, (1600, 424), mask=m2)
            background.save(save_img_folder + banner_string +

                            str(pfp_id) + '.png')

        if pfp3:
            m3 = Image.open(no_background_folder + str(pfp3) + '.png')
            m3 = m3.resize((int(m3.width*1.5), int(m3.height*1.5)))
            background.paste(m3, (1200, 424), mask=m3)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')
        if pfp4:
            m4 = Image.open(no_background_folder + str(pfp4) + '.png')
            m4 = m4.resize((int(m4.width*1.5), int(m4.height*1.5)))
            background.paste(m4, (800, 424), mask=m4)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        if pfp5:
            m5 = Image.open(no_background_folder + str(pfp5) + '.png')
            m5 = m5.resize((int(m5.width*1.5), int(m5.height*1.5)))
            background.paste(m5, (400, 424), mask=m5)
            background.save(save_img_folder + banner_string +
                            str(pfp_id) + '.png')

        background.paste(monke, (2000, 424), mask=monke)
        background.save(save_img_folder + banner_string + str(pfp_id) + '.png')

    return


def make_gif(gif, pfp_id):
    gif_string = gif.lower()
    url = (get_pfp_img_url(str(pfp_id)))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

    animated_gif = Image.open(gif_folder + gif_string + '.gif')
    frames = []
    m = Image.open(pfp_folder + str(pfp_id) + '.png')

    for f in ImageSequence.Iterator(animated_gif):

        frame = f.convert("RGBA")
        monke = m.copy()
        monke.paste(frame, mask=frame)
        # print(monke)
        frames.append(monke)

    if gif_string == 'welcome':
        frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                       '.gif', save_all=True, append_images=frames[1:],  loop=0, duration=500)
    else:
        frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                       '.gif', save_all=True, append_images=frames[1:],  loop=0)
    return


def make_gif_nb(gif, pfp_id):
    gif_string = gif.lower()

    animated_gif = Image.open(gif_folder + gif_string + '.gif')
    frames = []

    for f in ImageSequence.Iterator(animated_gif):
        m = Image.open(no_background_folder + str(pfp_id) + '.png')

        frame = f.convert("RGBA")
        monke = m.copy()
        monke.paste(frame, mask=frame)
        # print(monke)
        frames.append(monke)
    frames[0].save(save_img_folder + gif_string + str(pfp_id) +
                   '.gif', save_all=True, append_images=frames[1:],  loop=0)

    return


def high_quality_no_background(pfp_id):

    pfp = Image.open(no_background_folder + str(pfp_id) + '.png')
    monke = pfp.resize((int(pfp.width*5), int(pfp.height*5)))
    monke.save(save_img_folder + 'hq' + str(pfp_id) + '.png')

    return


def delete_gif(gif, pfp_id):
    gif_string = gif.lower()
    os.remove(save_img_folder + gif_string + str(pfp_id) + '.gif')


def delete_hq(pfp_id):
    os.remove(save_img_folder + 'hq' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')


def delete_smol(pfp_id):
    os.remove(save_img_folder + 'smol' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')


def make_b_w(pfp_id):
    url = (get_pfp_img_url(str(pfp_id)))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    monke = pfp.convert("LA")
    monke.save(save_img_folder + 'bw' + str(pfp_id) + '.png')

    return


def delete_bw(pfp_id):
    os.remove(save_img_folder + 'bw' + str(pfp_id) + '.png')
    os.remove(pfp_folder + str(pfp_id) + '.png')
