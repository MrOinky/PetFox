import discord
from discord.ext import commands
import sys, traceback, logging
import datetime, time, os, json
import asyncio, random

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
    
    @commands.command()
    async def fox(self, ctx):
        embed = discord.Embed(title="__Welcome to PetFox!__", colour=discord.Colour(0xf5a623), description="PetFox is a way to look after multiple cute foxes and earn rewards in doing so!", timestamp=datetime.datetime.utcfromtimestamp(time.time()))

        embed.set_footer(text="PetFox(FoxBot) by Mr_Oinky#6467", icon_url="https://cdn.discordapp.com/avatars/586640508772679681/e64788f49c5f602ce29b94eb0e32d75d.png?size=256")

        embed.add_field(name=":apple: Feed your foxes!", value="Foxes require feeding and a supply of water to be happy, make sure to keep them satisfied!", inline=True)
        embed.add_field(name=":volleyball: Play with your foxes!", value="As you play more, you will get rewards for your efforts!", inline=True)
        embed.add_field(name=":red_circle: Get Rewards!", value="A good owner needs rewards! Earn tokens and other items for happy foxes to buy better items!", inline=True)
        embed.add_field(name=":wrench: Commands", value=" Fox - Displays this message\n Buyfox - Buy a new fox, each costs more than the last!\n Shop - List the range of items you can buy for your foxes!\n Buy - Buy an item from the shop!\n Feed - Feed your foxes\n Play - Play with your foxes, don't forget to specify a toy!\n Stats - Display your stats.", inline=True)
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