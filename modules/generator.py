import guilded
from guilded.ext import commands
import asyncio
import json
import aiohttp
import random 
import os
import glob
import datetime
from tools.dataIO import fileIO

class Generator(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		author = message.author
		channel = message.channel
		guild = message.guild
		if author.bot:
			return
		await _check_values(author)
		await _check_values_ban(author)

async def _check_values(author):
	if not os.path.exists("users/{}".format(author.id)):
		os.makedirs("users/{}".format(author.id))
		time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
		new_account = {
			"player_name": "None",
			"player_health": 120,
			"player_max_health": 120,
			"inventory": {
				"silver": 0,
				"recipes": {},
				"items": {},
				"weapons": {},
				"materials": {},
				"locations_unlocked": ["starter area"],
				"healing_items": {}
			},
			"player_deaths": 0,
			"player_enemies_defeated": 0,
			"player_enemies_defeated_current_lifetime": 0,
			"player_weapon": "Fists",
			"current_enemy_health": 0,
			"current_enemy_name": "None",
			"setup": "False",
			"start_command_used": "False",
			"player_armor": "Rags",
			"player_location": "starter area"
		}
		fileIO("users/{}/info.json".format(author.id), "save", new_account)

async def _check_values_ban(author):
	if not os.path.exists("bans_tracker/{}".format(author.id)):
		os.makedirs("bans_tracker/{}".format(author.id))
		time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
		new_account = {
			"total_bans": 0,
			"last_ban": 0
		}
		fileIO("bans_tracker/{}/info.json".format(author.id), "save", new_account)

def setup(bot):
	bot.add_cog(Generator(bot))