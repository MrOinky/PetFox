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
def setsettings(filename, content):
    try:
        open(f"settings/{filename}.json", "x")
        json.dump(content,open(f"settings/{filename}.json","w"))
        logging.info(f"Created a new settings file - {filename}.json.")
    except:
        logging.info(f"skipping writing to {filename}.json, already exists.")

setsettings("core", {"prefix": "-"})
setsettings("cogs", ["cogs.petfox.petfox", "cogs.data.data", "cogs.currency.currency"])

with open("settings/core.json") as f:
    coresettings = json.load(f)
prefix = coresettings["prefix"]

bot = commands.Bot(command_prefix=prefix, activity=discord.Game("Booting PetFox!"))
logging.info(f"Booting into PetFox...")

with open("settings/cogs.json") as f:
    extensions = json.load(f)

if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except:
            logging.warn("Could not load {}".format(extension))
            raise
        else:
            logging.info("Successfully loaded cog {}".format(extension))

@bot.event
async def on_connect():
    logging.info(f"Connected to Discord. Now loading...")

@bot.event 
async def on_disconnect():
    logging.info(f"Discord connection has been closed.")

@bot.event
async def on_ready():
    logging.info(f"Booted successfully as: {bot.user.name} with id {bot.user.id}")
    logging.info(f"Thank you for using PetFox.")
    await bot.change_presence(activity=discord.Game("with foxes! Use -fox for help!"))

@bot.command(name="shutdown", aliases = ["close"])
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Closing PetFox v0.0.1 (base release) :wave:")
    logging.info(f"Shutting down PetFoxBot.")
    await bot.close()
    logging.info(f"Done.")
    exit()

@bot.command()
@commands.is_owner()
#this is entirely broken, DO NOT TOUCH
#if you want to edit the prefix as of now, use settings/core.json
#using this command will currently erase core.json and then prevent the bot from booting
async def prefix(ctx, prefix: str):
    json.dump(open("settings/core.json", "w"), {"prefix": prefix})
    await ctx.send("Updated bot prefix, restart the bot for this to take effect.")

#currently matches JdavisBro's FoxBot handler, will eventually change this to prompt help on a command.
@bot.event
async def on_command_error(ctx, error):
    if ctx.command != None:
        if ctx.command.name == "raiseLastError":
            raise error
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"The argument {error.param} is missing!")
        return
    await ctx.send(f"The following error occured while running {ctx.command.name}: `{error}`")
    bot.lastError = error

try:
    token = open("bottoken.txt", "r+").read()
except:
    logging.error(f"failed to find a token for the bot to login with, can not continue. Please insert a file into the PetFox directory called bottoken.txt with a valid bot token")
    logging.info(f"bot will now close.")
    exit()

bot.run(token, bot=True, reconnect=True)