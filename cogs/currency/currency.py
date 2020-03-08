import discord
from discord.ext import commands
import sys, traceback, logging
import datetime, time, os, json
import asyncio, random

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

def setup(bot):
    bot.add_cog(currency(bot))

try:
    open("dicts/basevalues/currency.json", "x")
    json.dump({"startingtokens": "100", "dailytokens": "150", "startinghoney": "0", "dailyhoney": "20"},open("settings/currency.json", "w"), indent=4)
    logging.info("Created currency.json.")
except:
    logging.info("found currency.json.")

try:
    open("storage/currency.json", "x")
    json.dump(dict(),open("storage/currency.json", "w"))
    logging.info("Created currency storage.")
except:
    logging.info("Found currency storage.")

class currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    