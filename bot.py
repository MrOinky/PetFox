import discord
from discord.ext import commands
import sys, traceback, logging
import time, os, json
import asyncio

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)
bot = commands.Bot(command_prefix="-", activity=discord.Game("Booting PetFox!"))
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
    await ctx.send("Closing PetFox v0.0.1 (the nothingness) :wave:")
    logging.info(f"Shutting down PetFoxBot.")
    await bot.close()
    logging.info(f"Done.")
    exit()

try:
    token = open("bottoken.txt", "r+").read()
except:
    logging.error(f"failed to find a token for the bot to login with, can not continue. Please insert a file into the PetFox directory called bottoken.txt with a valid bot token")
    logging.info(f"bot will now close.")
    exit()

bot.run(token, bot=True, reconnect=True)
