from discord.ext import commands
import discord
import json

with open('config.json') as f:
    config = json.load(f)
    
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

dc_tk = config['passkeys']['discord']