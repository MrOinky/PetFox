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

    def getValue(self, guildid: str, userid: str, value):
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
            return Storage[guildid][userid]["data"][value]

    def setValue(self, guildid: str, userid: str, value, newvalue):
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
            Storage[guildid][userid]["data"][value] = newvalue 

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
                                        "money": startmoney,
                                        "honey": starthoney,
                                        "nextpaydaytime": time.time()
                                       }
                                   }
        with open("storage/currency.json", "w+") as f:
            json.dump(Storage, f)
        await ctx.send("You have now set up your currency account!")
        logging.info("fully finished account setup for {user} in guild {guild}.".format(user=userid, guild=guildid))

    @commands.command()
    async def bal(self, ctx):
        """View your balance!"""
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
        if guildid not in Storage:
            await ctx.send("You do not have a currency account!")
            return
        if userid not in Storage[guildid].keys():
            await ctx.send("You do not have a currency account!")
            return
        money = currency.getValue(self,guildid,userid,"money")
        honey = currency.getValue(self,guildid,userid,"honey")
        embed = discord.Embed(title="Bank details for {}:".format(ctx.author.name), colour=discord.Colour(0x7ed321), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        embed.add_field(name=":red_circle: Tokens", value="You currently have {} tokens.".format(money))
        embed.add_field(name=":honey_pot: Honey", value="You currently have {} honey drops.".format(honey))

        await ctx.send(embed=embed)

    @commands.command()
    async def payday(self, ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("storage/currency.json", "r+") as f:
            bankDict = json.load(f)
        if guildid not in bankDict:
            bankDict[guildid] = {}
        if userid not in bankDict[guildid].keys():
            await ctx.send(f"You don't have a bank account! You can create one with `-newbank`")
            return
        if int(bankDict[guildid][userid]["data"]["nextpaydaytime"]) < datetime.datetime.now().timestamp():
            pass
        else:
            timeLeft = datetime.datetime.fromtimestamp(float(bankDict[guildid][userid]["data"]['nextpaydaytime']) - datetime.datetime.now().timestamp())
            timeLeft = timeLeft.strftime("%H hours, %M minutes and %S seconds")
            await ctx.send(f"You have to wait {timeLeft} until your next payday!")
            return
        bankDict[guildid][userid]["data"]["money"] = str(int(bankDict[guildid][userid]["data"]["money"])+int(currency.getSetting(self,"dailytokens")))
        bankDict[guildid][userid]["data"]["honey"] = str(int(bankDict[guildid][userid]["data"]["honey"])+int(currency.getSetting(self,"dailyhoney")))
        bankDict[guildid][userid]["data"]["nextpaydaytime"] = (datetime.datetime.now() + datetime.timedelta(hours=24)).timestamp()
        with open("storage/currency.json", "w+") as f:
            json.dump(bankDict,f)
        await ctx.send(f"{currency.getSetting(self,'dailytokens')} tokens and {currency.getSetting(self,'dailyhoney')} honey have been added to your account!")



        