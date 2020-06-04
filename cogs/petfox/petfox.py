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
        with open("storage/petfox.json", "w+") as f:    
            json.dump(Storage, f, indent=4)

    def setCurValue(self, guildid: str, userid: str, value, newvalue):
        with open("storage/currency.json", "r+") as f:
            Storage = json.load(f)
            Storage[guildid][userid]["data"][value] = newvalue
        with open("storage/currency.json", "w+") as f:
            json.dump(Storage, f, indent=4)

    def getItemValue(self, data: str):
        with open("dicts/basevalues/itemvalues.json", "r+") as f:
            Storage = json.load(f)
            return Storage[data]
    
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
                                    "items": 
                                       {
                                        "Basic Food": 10, 
                                        "Water": 5
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
            json.dump(Storage, f, indent = 4)
        await ctx.send("You have now set up your foxpet account!")
        await asyncio.sleep(1)
        await ctx.send("You also need to run -newbank now to set up your currency, then you have completed your setup process.")
        logging.info("finished petfox account setup for {user} in guild {guild}.".format(user=userid, guild=guildid))

    @commands.command()
    async def shop(self, ctx, category = "all"):
        """
        Displays the shop items in a neat order.

        Currently testing this new system rather than a giant embed chunk.
        This is the main reason lots of new item values exist.
        """

        embed = discord.Embed(title="Shop", colour=discord.Colour(0x4a90e2), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        with open("dicts/basevalues/itemvalues.json", "r+") as f:
            itemvalues = json.load(f)

        foodtitle = False
        caretitle = False
        toystitle = False

        for i in itemvalues.keys():
            item = petfox.getItemValue(self, i)
            if category == "all" or category == "Food":
                if item[5] == "Food":
                    if foodtitle == False:
                        embed.add_field(name=":meat_on_bone: Food", value="Use these to keep your foxes full and hydrated!", inline=False)
                        foodtitle = True
                    embed.add_field(name=f"{item[4]} {i[0].upper() + i[1:]}", value=f":red_circle:Costs {item[3]} tokens.\n:meat_on_bone:+{item[0]}% Hunger.\n:droplet:-{item[1]}% Thirst.")
        for i in itemvalues.keys():
            item = petfox.getItemValue(self, i)
            if category == "all" or category == "Care":
                if item[5] == "Care":
                    if caretitle == False:
                        embed.add_field(name=":green_heart: Care", value="Use these to keep your foxes clean and healthy!", inline=False)
                        caretitle = True
                    embed.add_field(name=f"{item[4]} {i[0].upper() + i[1:]}", value=f":red_circle:Costs {item[3]} tokens.")
        for i in itemvalues.keys():
            item = petfox.getItemValue(self, i)
            if category == "all" or category == "Toys":
                if item[5] == "Toys":
                    if toystitle == False:
                        embed.add_field(name=":yarn: Toys", value="Use these to keep your foxes happy!", inline=False)
                        toystitle = True
                    embed.add_field(name=f"{item[4]} {i[0].upper() + i[1:]}", value=f":red_circle:Costs {item[3]} tokens.")
        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        embed = discord.Embed(title="Fox Status", colour=discord.Colour(0xf5a623), description=":poultry_leg:Fullness\nYour foxes are {fullness}% full.\n:cup_with_straw:Thirst\nYour foxes are {thirst}% thirsty.\n:fox:Foxes\nYou have {foxcount} foxes.\nYour next fox is priced at {nextprice} tokens.".format(fullness = petfox.getValue(self,guildid,userid,"foxdata","fullness"), thirst = petfox.getValue(self,guildid,userid,"foxdata","thirst"), foxcount = petfox.getValue(self,guildid,userid,"foxdata","foxes"), nextprice = petfox.getValue(self,guildid,userid,"foxdata","foxes") * 500), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        await ctx.send(embed=embed)
    @commands.command()
    async def inventory(self, ctx, category = "all"):
        """See your cool items!"""
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)
        embed = discord.Embed(title="Inventory", colour=discord.Colour(0xf5a623), timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="Pet Fox by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        with open("storage/petfox.json", "r+") as f:
            Storage = json.load(f)

        with open("dicts/basevalues/itemvalues.json", "r+") as f:
            itemvalues = json.load(f)

        foodtitle = False
        caretitle = False
        toystitle = False

        for i in Storage[guildid][userid]["items"].keys():
            item = petfox.getItemValue(self, i)
            amount = petfox.getValue(self, guildid, userid, "items", i)
            if category == "all" or category == "Food":
                if item[5] == "Food":
                    if foodtitle == False:
                        embed.add_field(name=":meat_on_bone: Food", value="Use these to keep your foxes full and hydrated!", inline=False)
                        foodtitle = True
                    embed.add_field(name=f"{item[4]} {i[0].upper() + i[1:]}", value=f"You have {amount} servings.\n:meat_on_bone:+{item[0]}% Hunger.\n:droplet:-{item[1]}% Thirst.", inline=True)
        for i in Storage[guildid][userid]["items"].keys():
            item = petfox.getItemValue(self, i)
            amount = petfox.getValue(self, guildid, userid, "items", i)
            if category == "all" or category == "Care":
                if item[5] == "Care":
                    if caretitle == False:
                        embed.add_field(name=":green_heart: Care", value="Use these to keep your foxes clean and healthy!", inline=False)
                        caretitle = True
                    embed.add_field(name=f"{item[4]} {i[0].upper() + i[1:]}", value=f"You have {amount} Uses.", inline=True)
        for i in Storage[guildid][userid]["items"].keys():
            item = petfox.getItemValue(self, i)
            amount = petfox.getValue(self, guildid, userid, "items", i)
            if category == "all" or category == "Toys":
                if item[5] == "Toys":
                    if toystitle == False:
                        embed.add_field(name=":yarn: Toys", value="Use these to keep your foxes happy!", inline=False)
                        toystitle = True
                    embed.add_field(name=f"{item[4]} {i[0].upper() + i[1:]}", value=f"You have {amount} Left.", inline=True)

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
    #this is very questionable
    @commands.command()
    async def play(self, ctx):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)

        mood = random.choice(["happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "happy", "veryhappy", "sad", "sad", "sad", "sad", "sad", "sad", "sad", "sad"])
        happy = petfox.getValue(self, guildid, userid, "foxdata", "happiness")

        if mood == "happy":
            await ctx.send("Your foxes had a nice time playing with you.")
            newhappy = happy + 0.4
            petfox.setValue(self, guildid, userid, "foxdata", "happiness", newhappy)
        elif mood == "veryhappy":
            await ctx.send("You and your foxes had loads of fun playing together!")
            newhappy = happy + 1.1
            petfox.setValue(self, guildid, userid, "foxdata", "happiness", newhappy)
        elif mood == "sad":
            await ctx.send("Your foxes didn't enjoy playing that much.")
    #remember that food codes are HUNGER, THIRST, HAPPINESS
    #only currently allows single feeds.
    @commands.command()
    async def feed(self, ctx, food: str):
        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)

        food = food.lower()

        try:
            fooditem = petfox.getItemValue(self, food)
        except KeyError:
            await ctx.send(f"Whoops! looks like {food[0].upper() + food[1:]} doesnt exist!")
            return

        if fooditem[5] != "Food":
            await ctx.send(f"{food[0].upper() + food[1:]} is not a food!")
            return "notfood"

        try:
            amt = petfox.getValue(self, guildid, userid, "items", food) 
        except KeyError:
            await ctx.send(f"You do not have any {food[0].upper() + food[1:]}")
            return

        amt = amt - 1

        petfox.setValue(self, guildid, userid, "items", food, amt)

        hu = fooditem[0]
        logging.info(str(hu))
        t = fooditem[1]
        logging.info(str(t))
        ha = fooditem[2]
        logging.info(str(ha))

        hu = min(int(hu) + petfox.getValue(self, guildid, userid, "foxdata", "fullness"), 100)
        logging.info(str(hu))
        t = max(petfox.getValue(self, guildid, userid, "foxdata", "thirst") - int(t), 0)
        logging.info(str(t))
        ha = min(petfox.getValue(self, guildid, userid, "foxdata", "happiness") + int(ha), 255)
        logging.info(str(ha))

        petfox.setValue(self, guildid, userid, "foxdata", "fullness", hu)
        petfox.setValue(self, guildid, userid, "foxdata", "thirst", t)
        petfox.setValue(self, guildid, userid, "foxdata", "happiness", ha)

        lemon = food[0].upper()  

        logging.info(f"{lemon}")
        if lemon == "A":
            await ctx.send(f"You fed your foxes an {food[0].upper() + food[1:]}.")
        elif lemon == "E":
            await ctx.send(f"You fed your foxes an {food[0].upper() + food[1:]}.")
        elif lemon == "I":
            await ctx.send(f"You fed your foxes an {food[0].upper() + food[1:]}.")
        elif lemon == "O":
            await ctx.send(f"You fed your foxes an {food[0].upper() + food[1:]}.")
        elif lemon == "U":
            await ctx.send(f"You fed your foxes an {food[0].upper() + food[1:]}.")        
        else:
            await ctx.send(f"You fed your foxes a {food[0].upper() + food[1:]}.")
    @commands.command()
    async def buy(self, ctx, i: str):

        guildid = str(ctx.guild.id)
        userid = str(ctx.author.id)

        i = i.lower()

        try:
            item = petfox.getItemValue(self, i)
        except KeyError:
            await ctx.send(f"{i[0].upper() + i[1:]} is not an item!")
            return

        try:
            money = petfox.getCurValue(self, guildid, userid, "money")
        except KeyError:
            await ctx.send("Whoops! I cant find the money variable for your account, make sure youve done -start and -newbank before!")
            return
        
        try:
            cost = item[3]
        except KeyError:
            await ctx.send("Uh Oh! Looks like this item has a malformed json entry, please inform the bot/fork author of this if you have not modified itemvalues.json in any way!")
            return

        money = int(money)

        if money - cost < 0:
            await ctx.send(f"You need {cost} tokens to afford {i[0].upper() + i[1:]} but only have {money}!")
            return
        else:
            money = money - cost
            petfox.setCurValue(self, guildid, userid, "money", money)
            try:
                amt = petfox.getValue(self, guildid, userid, "items", i)
            except KeyError:
                amt = 0
            amt = amt + 1
            petfox.setValue(self, guildid, userid, "items", i, amt)

            lemon = i[0].upper()   

            if lemon == "A":
                await ctx.send(f"You just bought an {i[0].upper() + i[1:]}, bringing your total to {amt}!")
            elif lemon == "E":
                await ctx.send(f"You just bought an {i[0].upper() + i[1:]}, bringing your total to {amt}!")
            elif lemon == "I":
                await ctx.send(f"You just bought an {i[0].upper() + i[1:]}, bringing your total to {amt}!")
            elif lemon == "O":
                await ctx.send(f"You just bought an {i[0].upper() + i[1:]}, bringing your total to {amt}!")
            elif lemon == "U":
                await ctx.send(f"You just bought an {i[0].upper() + i[1:]}, bringing your total to {amt}!")
            else:
                await ctx.send(f"You just bought a {i[0].upper() + i[1:]}, bringing your total to {amt}!")
