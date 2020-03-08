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
    json.dump({"startingtokens": "100", "dailytokens": "150", "startinghoney": "0", "dailyhoney": "20"},open("dicts/basevalues/currency.json", "w"), indent=4)
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

    def getSetting(self, setting: str):
        with open("dicts/basevalues/currency.json", "r+") as f:
            settings = json.load(f)
            return settings[setting]

    @commands.command()
    async def newbank(self, ctx):
        """Create your account!"""
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
        if guildid not in Storage:
            Storage[guildid] = {}
            logging.info("Added guildid {} to storage".format(guildid))
        if userid in Storage[guildid].keys():
            await ctx.send("You have already made an account!")
            return
        startmoney = currency.getSetting(self,"startingtokens")
        starthoney = currency.getSetting(self,"startinghoney")
        Storage[guildid][userid] = {
                                    "data": 
                                       {
                                        "moneyearnt": 0,
                                        "highestmoney": startmoney,
                                        "honeyearnt": 0,
                                        "highesthoney": starthoney,
                                        "currentmoney": startmoney,
                                        "currenthoney": starthoney
                                       }
                                   }
        with open("storage/currency.json", "w+") as f:
            json.dump(Storage, f)
        await ctx.send("You have now set up your currency account!")
        logging.info("fully finished account setup for {user} in guild {guild}.".format(user=userid, guild=guildid))

        