import discord
from discord.ext import commands
import sys, traceback, logging
import time, os, json
import asyncio

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

#setup of folders, makes some ones necessary now, and some necessary in the future.
#this is done so that the bot can entirely regenerate the base structure in the event something goes wrong.
if not os.path.isdir("settings"):
    os.mkdir("settings")
    logging.info(f"Created dir - settings")
    logging.warning(f"if you have ran the bot and saved settings before this should NOT happen, and will be a sign of loss of settings.")
if not os.path.isdir("dicts"):
    os.mkdir("dicts")
    logging.info(f"Created dir - dicts")
    logging.warning(f"If you have ran the bot and added custom dictionaries before this should NOT happen, and will be a sign of loss of dictionaries, base dicts are set to auto regenerate.")
if not os.path.isdir("storage"):
    os.mkdir("storage")
    logging.info(f"Created dir - storage")
    logging.warning(f"If you have ran the bot and saved data before this should NOT happen, and will be a sign of loss of data.")
if not os.path.isdir("dicts/basevalues"):
    os.mkdir("dicts/basevalues")
    logging.info("created dir - dicts/basevalues")
#create the settings file where it is required
#manages both the core settings and PetFox settings (on a cog by cog basis)
#system very similar to (if not the same as) JdavisBro's FoxBot settings system
def locatesettings(filename, content):
    try:
        open(f"settings/{filename}.json", "x")
        json.dump(content,open(f"settings/{filename}.json","w"))
        logging.info(f"Created a new settings file - {filename}.json.")
    except:
        logging.info(f"skipping writing to {filename}.json, already exists.")

locatesettings("core", {"prefix": "-"})

with open("settings/core.json") as f:
    coresettings = json.load(f)
prefix = coresettings["prefix"]

bot = commands.Bot(command_prefix=prefix, activity=discord.Game("Booting PetFox!"))
logging.info(f"Booting into PetFox...")

@bot.event
async def on_connect():
    logging.info(f"Connected to Discord. Now loading...")

@bot.event 
async def on_disconnect():
    logging.info(f"Discord connection has been lost or closed.")

@bot.event
async def on_ready():
    logging.info(f"Booted successfully as: {bot.user.name} with id {bot.user.id}")
    logging.info(f"Thank you for using PetFox.")
    await bot.change_presence(activity=discord.Game("with foxes!"))

@bot.command(name="shutdown", aliases = ["close"])
async def shutdown(ctx):
    await ctx.send("Closing PetFox v0.0.1 (now with files (and no petfox)) :wave:")
    logging.info(f"Shutting down PetFoxBot.")
    await bot.close()
    logging.info(f"Done.")
    exit()

@bot.command()
async def prefix(ctx, prefix: str):
    with open("settings/core.json") as f:
        file = json.load(f)
    oprefix = file["prefix"]
    json.dump("settings/core.json", {"prefix": prefix})
    await ctx.send("Updated bot prefix, restart the bot for this to take effect.")

@bot.event
async def on_command_error(ctx, error):
    if ctx.command.name == "raiseLastError":
        raise error
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.send(f"`{error} occured while running {ctx.command.name}`")
    bot.lastError = error

try:
    token = open("bottoken.txt", "r+").read()
except:
    logging.error(f"failed to find a token for the bot to login with, can not continue. Please insert a file into the PetFox directory called bottoken.txt with a valid bot token")
    logging.info(f"bot will now close.")
    exit()

bot.run(token, bot=True, reconnect=True)
