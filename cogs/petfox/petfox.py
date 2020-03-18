import discord
from discord.ext import commands
import sys, traceback, logging
import datetime, time, os, json
import asyncio, random

from cogs import currency

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

def setup(bot):
    bot.add_cog(petfox(bot))

try:
    open("storage/petfox.json", "x")
    json.dump(dict(),open("storage/petfox.json", "w"))
    logging.info("Created petfox storage.")
except:
    logging.info("Found petfox storage.")

#regenerator for all edible item values via feed
#all values are stored as a list of three as so:
#["HUNGERVALUE","THIRSTVALUE","HAPPINESS"]
#remember that hunger and happiness add on, and thirst takes off by default, only use negatives in the case you want to go the opposite way.
try:
    open("dicts/basevalues/foodvalues.json", "x")
    json.dump({"basicfood": ["2", "0", "0"], "sweetfood": ["3", "0", "0.1"], "nutrientfood": ["5", "0", "0"], "berry": ["8", "1", "0.2"], "meatbites": ["12", "0", "0.1"], "pancake": ["9", "0", "0.4"], "waffle": ["11", "0", "0.3"], "apple": ["10", "2", "0.2"], "salad": ["14", "0", "0"], "amateurkibble": ["7", "0", "0.05"], "mchoccookie": ["13", "0", "0.5"], "wchockcookie": ["14", "0", "0.6"], "water": ["0", "6", "0"], "milk": ["0", "9", "0.05"], "icedwater": ["0", "7", "0.1"]}, open("dicts/basevalues/foodvalues.json", "w"), indent=4)
    logging.info("Created foodvalues.json.")
except:
    logging.info("Found foodvalues.json.")

class petfox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def getValue(self, guildid: str, userid: str, data: str, value):
        with open("storage/petfox.json", "r+") as f:
            Storage = json.load(f)
            return Storage[guildid][userid][data][value]

    def getCurValue(self, guildid: str, userid: str, value):
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
            return Storage[guildid][userid]["data"][value]

    def setValue(self, guildid: str, userid: str, data: str, value, newvalue):
        with open("storage/petfox.json", "r+") as f:
            Storage = json.load(f)
            Storage[guildid][userid][data][value] = newvalue

    def setValue(self, guildid: str, userid: str, value, newvalue):
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
            Storage[guildid][userid]["data"][value] = newvalue  
    
    @commands.command()
    async def fox(self, ctx):
        embed = discord.Embed(title="__Welcome to PetFox!__", colour=discord.Colour(0xf5a623), description="PetFox is a way to look after multiple cute foxes and earn rewards in doing so!", timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="PetFox(FoxBot) by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        embed.add_field(name=":apple: Feed your foxes!", value="Foxes require feeding and a supply of water to be happy, make sure to keep them satisfied!", inline=True)
        embed.add_field(name=":volleyball: Play with your foxes!", value="As you play more, you will get rewards for your efforts!", inline=True)
        embed.add_field(name=":red_circle: Get Rewards!", value="A good owner needs rewards! Earn tokens and other items for happy foxes to buy better items!", inline=True)
        embed.add_field(name=":wrench: Commands", value=" fox - Displays this message\n start - Setup your account, run this before doing anything else.\n bal - view your bank balance, both your honey and token statistics.\n buyfox - Buy a new fox, each costs more than the last!\n shop - List the range of items you can buy for your foxes!\n buy - Buy an item from the shop!\n feed - Feed your foxes\n play - Play with your foxes, don't forget to specify a toy!\n stats - Display your stats.", inline=True)
        embed.add_field(name=":bug: Bugs", value="In the event of an issue, \nmake sure to report it so\nyou can get the best\nexperience!", inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def start(self, ctx):
        """Create your account!"""
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        with open("storage/petfox.json", "r+") as f:
            Storage = json.load(f)
        if guildid not in Storage:
            Storage[guildid] = {}
            logging.info("Added guildid {} to storage".format(guildid))
        if userid in Storage[guildid].keys():
            await ctx.send("You have already made an account!")
            return
        Storage[guildid][userid] = {"foxdata": 
                                       {
                                        "foxes": 1, 
                                        "thirst": 20, 
                                        "fullness": 80, 
                                        "happiness":75.0
                                       },
                                    "supplies": 
                                       {
                                        "basicfood": 10, 
                                        "water": 5
                                       },
                                    "badges": {},
                                    "foxes": {}, 
                                    "data": 
                                       {
                                        "totalfeeds": 0, 
                                        "totaldrinks": 0, 
                                        "timesplayed": 0, 
                                        "battles": 0,
                                        "itemsbought": 0
                                       }
                                   }
        with open("storage/petfox.json", "w+") as f:
            json.dump(Storage, f)
        await ctx.send("You have now set up your foxpet account!")
        await asyncio.sleep(1)
        await ctx.send("You also need to run -newbank now to set up your currency, then you have completed your setup process.")
        logging.info("finished petfox account setup for {user} in guild {guild}.".format(user=userid, guild=guildid))

    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title="Shop", colour=discord.Colour(0x4a90e2), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        embed.add_field(name=":cup_with_straw: Water", value="5 Tokens each.", inline=True)
        embed.add_field(name=":canned_food: Basic Food", value="5 Tokens per serving.", inline=True)
        embed.add_field(name=":milk: Milk", value="15 Tokens each.", inline=True)
        embed.add_field(name=":candy: Sweet Food", value="20 Tokens per serving.", inline=True)
        embed.add_field(name=":leafy_green: Nutrient Food", value="25 Tokens per serving.", inline=True)
        embed.add_field(name=":strawberry: Berry", value="35 Tokens each.", inline=True)
        embed.add_field(name=":cut_of_meat: Meat Bites", value="40 Tokens per serving.", inline=True)
        embed.add_field(name="<:waterglass:682713750201040906> Iced Water", value="25 Tokens each.", inline=True)
        embed.add_field(name=":pancakes: Pancakes", value="100 Tokens each.", inline=True)
        embed.add_field(name=":waffle: Waffles", value="100 Tokens each.", inline=True)
        embed.add_field(name=":apple: Apple", value="60 Tokens each.", inline=True)
        embed.add_field(name=":salad: Salad", value="55 Tokens per serving.", inline=True)
        embed.add_field(name=":canned_food: Amateur Kibble", value="45 Tokens per serving.", inline=True)
        embed.add_field(name=":cookie: Milk Choc Cookie", value="125 Tokens each.", inline=True)
        embed.add_field(name="<:whitecookie:682713693489725443> White Choc Cookie", value="150 Tokens each.", inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        embed = discord.Embed(title="Fox Status", colour=discord.Colour(0xf5a623), description=":poultry_leg:Fullness\nYour foxes are {fullness}% full.\n:cup_with_straw:Thirst\nYour foxes are {thirst}% thirsty.\n:fox:Foxes\nYou have {foxcount} foxes.\nYour next fox is priced at {nextprice} tokens.".format(fullness = petfox.getValue(self,guildid,userid,"foxdata","fullness"), thirst = petfox.getValue(self,guildid,userid,"foxdata","thirst"), foxcount = petfox.getValue(self,guildid,userid,"foxdata","foxes"), nextprice = petfox.getValue(self,guildid,userid,"foxdata","foxes") * 500), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        await ctx.send(embed=embed)
    @commands.command()
    async def inventory(self, ctx):
        """See your cool items!"""
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        embed = discord.Embed(title="Inventory", colour=discord.Colour(0xf5a623), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        with open("storage/petfox.json", "r+") as f:
            Storage = json.load(f)

        for item in Storage[guildid][userid]["supplies"].keys():
            logging.info("adding field for {}".format(item))
            embed.add_field(name=item, value="You have {amount} {item}s".format(amount=petfox.getValue(self, guildid, userid, "supplies", item), item=item))
        
        await ctx.send(embed=embed)
    @commands.command()
    async def buyfox(self, ctx, amount: int):
        """
        Buy an amount of Foxes to add to your collection.

        Each fox costs more than the last!
        """
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)

        buymore = True
        
        while buymore:
            foxcount = petfox.getValue(self, guildid, userid, "foxdata", "foxes")
            money = petfox.getCurValue(self, guildid, userid, "money")
            honey = petfox.getCurValue(self, guildid, userid, "honey")
            cost = 500 * foxcount
            hcost = 50 + max(foxcount - 9, 0) * 10000
            newcount = foxcount + 1
            if cost > int(money) or hcost > int(honey):
                await ctx.send("You need {cost} tokens and {honey} honey to afford a new fox, but you can not afford that!".format(cost=cost, honey=hcost))
                await asyncio.sleep(1)
                await ctx.send("Cancelling purchase.")
                return
            else:
                petfox.setValue(self, guildid, userid, "foxdata", "foxes", newcount)
                newmoney = money - cost
                newhoney = honey - hcost
                petfox.setCurValue(self, guildid, userid, "money", newmoney)
                petfox.setCurValue(self, guildid, userid, "honey", newhoney)
        

            if int(amount) > 1:
                buymore = True
                amount = amount - 1
                await ctx.send("you bought a fox for {cost} tokens and {honey} honey taking your total foxes to {count}, and you are buying {amount} more.".format(cost = cost, honey = hcost, count = newcount, amount = amount))
                await asyncio.sleep(1)
                await ctx.send("Buying another fox in 5 seconds.")
                await asyncio.sleep(5)
            else:
                buymore = False
                await ctx.send("you bought a fox for {cost} tokens and {honey} honey taking your total foxes to {count}, and are not buying any more.".format(cost = cost, honey = hcost, count = newcount))
                await asyncio.sleep(1)
                cost = 500 * foxcount
                hcost = hcost = 50 + max(foxcount - 9, 0) * 10000
                await ctx.send("your next fox is now priced at {cost} tokens and {honey} honey.".format(cost = cost, honey = hcost))
