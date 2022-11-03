import guilded
from guilded.ext import commands
import asyncio
import json
import aiohttp
import random 
from tools.dataIO import fileIO

with open('config/config.json') as f:
    config = json.load(f)

prefix = config["Prefix"]

class Help(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command()
	async def help(self, ctx, *, num: int=None):
		if num == None:
			em = guilded.Embed(title="Guilded RPG - Help menu", description=f"`{prefix}start` - Start playing Guilded RPG!\n`{prefix}fight` - Explore & fight enemies.\n`{prefix}profile` - View your characters profile, and stats.\n`{prefix}travel` - Travel to other locations.\n`{prefix}equip` - Equip other things.\n`{prefix}npc` - Get a list of the NPC's in your area.\n`{prefix}inventory` - Check your inventory.\n\n[Invite Guilded RPG](https://www.guilded.gg/b/8f16b207-3de1-4167-aeca-8d3f9b6c90f0)\n[Support server](https://www.guilded.gg/i/EoeBjyqk)", color=0x363942)
			await ctx.send(embed=em)

def setup(bot):
	bot.remove_command('help')
	bot.add_cog(Help(bot))