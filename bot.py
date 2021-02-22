import discord 
from discord.ext import commands 
import json
from pathlib import Path
import logging 
import datetime
import os

import cogs._json

cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")

def get_prefix(bot, message):
    data = cogs._json.read_json('prefixes')
    if not str(message.guild.id) in data:
        return commands.when_mentioned_or('/')(bot, message)
    return commands.when_mentioned_or(data[str(message.guild.id)])(bot, message)

secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, owner_id=398264990567628812)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.version = '0.0.5'

bot.blacklisted_users = []

bot.cwd = cwd

bot.colours = {
    'WHITE': 0xFFFFFF,
  'AQUA': 0x00FFFF,
  'GREEN': 0x008000,
  'BLUE': 0x0000FF,
  'PURPLE': 0x800080,
  'DEEP_PINK': 0xFF1493,
  'GOLD': 0xFFD700,
  'ORANGE': 0xFFA500,
  'RED': 0xFF0000,
  'NAVY': 0x000080,
  'DARK_AQUA': 0x66CDAA,
  'DARK_GREEN': 0x006400,
  'DARK_BLUE': 0x00008B,
  'DARK_PURPLE': 0x663399,
  'HOT_PINK': 0xFF69B4,
  'DARK_ORANGE': 0xFF8C00,
  'DARK_RED': 0xFF8C00,
  'CYAN': 0x00FFFF,
  'LIME_GREEN': 0x00FF00,
}
bot.colour_list = [c for c in bot.colours.values()]

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: /\n-----")
    await bot.change_presence(activity=discord.Game(name=f"Hi, my names {bot.user.name}.\nUse / to interact with me!")) # This changes the bots 'activity'

@bot.event
async def on_message(message):
    #ignore ourselves
    if message.author.id == bot.user.id:
        return

    #blacklist system
    if message.author.id in bot.blacklisted_users:
        return

    if bot.user.mention in message.content:
        data = cogs._json.read_json('prefixes')
        if str(message.guild.id) in data:
            prefix = data[str(message.guild.id)]
        else:
            prefix = '/'
        prefixMsg = await message.channel.send("My prefix is **`{prefix}`**")
        await prefixMsg.add_reaction('✅')

    await bot.process_commands(message)

if __name__ == '__main__':
    for file in os.listdir(cwd+"/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            bot.load_extension(f"cogs.{file[:-3]}")
    bot.run(bot.config_token)
