from aiohttp import web
from config import gen2List, gen3List #type: ignore
import aiohttp
import asyncio
from PIL import Image
from io import BytesIO

routes = web.RouteTableDef()

async def common_color(img: Image) -> tuple:
    pixels = await asyncio.get_event_loop().run_in_executor(None, img.getcolors)
    most_common = max(pixels, key=lambda x: x[0])
    return most_common[1]

@routes.get("/image")
async def image(request):
    try:
        gen = int(request.rel_url.query['gen'])
        id = int(request.rel_url.query['id'])
        background = True if request.rel_url.query['bg'] == "true" else False
    except :
        return web.Response(text="Invalid Variables",status=400)
    if gen == 2:
        for i in gen2List:
            if int(i['mint']["name"].split("#")[1]) == id:
                monke = i
                async with aiohttp.ClientSession() as session:
                    async with session.get(i['mint']['imageUri']) as resp:
                        img = await resp.read()
                        img = await asyncio.get_event_loop().run_in_executor(None, Image.open, BytesIO(img))
                break
    if background:
        bg = await common_color(img)
        pixels = await asyncio.get_event_loop().run_in_executor(None, img.getdata)
        newpixels = []
        for pixel in pixels:
            if pixel == bg:
                newpixels.append((0,0,0,0))
            else:
                newpixels.append(pixel)
        img.putdata(newpixels)
    
    imgbytes = BytesIO()
    img.save(imgbytes, format="PNG")
    
    return web.Response(body=imgbytes.getvalue(), content_type="image/png")

app = web.Application()
app.add_routes(routes)