from discord.ext import commands
import discord
import json
import socket

with open('config.json') as f:
    config = json.load(f)
    
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

cache = {}

dc_tk = config['passkeys']['discord']

tensor_tk = config['passkeys']['tensor']

with open('monkeList.json') as f:
    gen2List = json.load(f)
    
gen3List = {}

helius_tk = config['passkeys']['helius']

try:
    base = socket.gethostbyname(socket.gethostname())
except:
    base = ''
if not base or base.startswith('127.'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('4.2.2.1', 0))
    base = s.getsockname()[0]