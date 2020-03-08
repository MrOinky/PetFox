import discord
from discord.ext import commands
import sys, traceback, logging
import datetime, time, os, json
import asyncio, random

logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)

def setup(bot):
    bot.add_cog(petfox(bot))

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