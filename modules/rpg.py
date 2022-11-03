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
from modules.generator import _check_values

class Rep(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	#-----------------------------------------------------------------------------#
	#-------------------------------CONFIG COMMANDS-------------------------------#
	#-----------------------------------------------------------------------------#

	@commands.command()
	async def file(self, ctx):
		author = ctx.author
		if author.bot:
			return
		await _check_values(author)
		info = fileIO("users/{}/info.json".format(author.id), "load")
		em = guilded.Embed(title="{}'s file.".format(author.name), description="{}".format(info), color=0x363942)
		await ctx.send(embed=em)

	#--------------------------------------------------------------------------#
	#-------------------------------RPG COMMANDS-------------------------------#
	#--------------------------------------------------------------------------#

	@commands.command()
	async def start(self, ctx):
		author = ctx.author
		if author.bot:
			return
		await _check_values(author)
		info = fileIO("users/{}/info.json".format(author.id), "load")
		enemies = fileIO("enemies/enemies.json", "load")
		if info["setup"] == "False":
			em = guilded.Embed(description="`Unknown:` Help! This slimey monster is being a pest! Please kill it!", color=0x363942)
			await ctx.send(embed=em)
			info["current_enemy_health"] = 1
			info["current_enemy_name"] = "small green slime"
			fileIO("users/{}/info.json".format(author.id), "save", info)
			enemy_display_name = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["display_name"]
			enemy_max_health = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["enemy_max_health"]
			em = guilded.Embed(title="{}'s fight information:".format(author.name), description="{}\n`Health:` {}/{}".format(enemy_display_name, info["current_enemy_health"], enemy_max_health), color=0x363942)
			em.set_footer(text="Use .fight to battle the {}".format(enemy_display_name))
			await ctx.send(embed=em)
			info["start_command_used"] = "True"
			fileIO("users/{}/info.json".format(author.id), "save", info)
		else:
			em = guilded.Embed(title="Woah there {}".format(author.name), description="You've already setup your character!", color=0x363942)
			await ctx.send(embed=em)

	@commands.command()
	async def fight(self, ctx):
		author = ctx.author
		message = ctx.message
		channel = ctx.channel
		if author.bot:
			return
		await _check_values(author)
		info = fileIO("users/{}/info.json".format(author.id), "load")
		if info["start_command_used"] == "True" and info["setup"] == "False":
			await start_tutorial_part_1(self, ctx)
		elif info["start_command_used"] == "True" and info["setup"] == "True":
			await fight_stuff(self, ctx)

async def start_tutorial_part_1(self, ctx):
	author = ctx.author
	message = ctx.message
	channel = ctx.channel
	info = fileIO("users/{}/info.json".format(author.id), "load")
	enemies = fileIO("enemies/enemies.json", "load")
	weapons = fileIO("weapons/weapons.json", "load")
	enemy_display_name = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["display_name"]
	player_damage = random.randint(weapons[info["player_weapon"]]["min_damage"], weapons[info["player_weapon"]]["max_damage"])
	player_damage = player_damage
	enemy_damage = random.randint(enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["enemy_min_damage"], enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["enemy_max_damage"])
	enemy_damage = enemy_damage
	player_health = info["player_health"] - enemy_damage
	enemy_health = info["current_enemy_health"] - player_damage
	em = guilded.Embed(title="{} fights {}.".format(author.name, enemy_display_name), description="`PLAYER'S LOGS`\nDamage to enemy: {}\nDamage taken: {}\nPlayer health: {}/{}\n\n`{}'S LOGS`\nDamage to player: {}\nDamage taken: {}\nHealth: {}".format(player_damage, enemy_damage, player_health, info["player_max_health"], info["current_enemy_name"].upper(), enemy_damage, player_damage, enemy_health), color=0x363942)
	await ctx.send(embed=em)
	if enemy_health <= 0:
		em = guilded.Embed(title="Enemy defeated", description="`Unknown:` Wow, thanks traveler!\n`Unknown:` Say, what is your name? My name is Leya.\n\nType out your player name. No command needed.", color=0x363942)
		em.set_footer(text="Ex: Beezo")
		await ctx.send(embed=em)
		def pred(m):
			return m.author == message.author and m.channel == message.channel
		answer1 = await self.bot.wait_for("message", check=pred)
		info["player_name"] = str(answer1.content)
		info["setup"] = "True"
		info["current_enemy_name"] = "None"
		info["current_enemy_health"] = 0
		if "worn shortsword" not in info["inventory"]["weapons"]:
			info["inventory"]["weapons"]["worn shortsword"] = {
				"amount": 1
			}
		if "lite health potion" not in info["inventory"]["healing_items"]:
			info["inventory"]["healing_items"]["lite health potion"] = {
				"amount": 3
			}
		fileIO("users/{}/info.json".format(author.id), "save", info)
		em = guilded.Embed(description="`Leya:` Well it's nice to meet you {}! If you ever need me, just use `.npc` at Starter area.\n\n`Leya heals you for your efforts.`".format(info["player_name"]), color=0x363942)
		await ctx.send(embed=em)
		em = guilded.Embed(title="Intro completed.", description="**Items obtained:**\nx1 Worn shortsword\nx3 Lite health potion", color=0x363942)
		await ctx.send(embed=em)

async def fight_stuff(self, ctx):
	author = ctx.author
	message = ctx.message
	channel = ctx.channel
	info = fileIO("users/{}/info.json".format(author.id), "load")
	enemies = fileIO("enemies/enemies.json", "load")
	weapons = fileIO("weapons/weapons.json", "load")
	if info["current_enemy_name"] == "None":
		enemies_list = []
		for i in enemies["locations"][info["player_location"]]["enemies"]:
			enemies_list.append(i)
		selected_enemy = random.choice(enemies_list)
		selected_enemy = selected_enemy
		em = guilded.Embed(description="{} wanders around {}, and finds a {}\n\nWould you like to fight it?".format(info["player_name"], info["player_location"], selected_enemy), color=0x363942)
		em.set_footer(text="Valid text options: Yes, No, Y, N")
		await ctx.send(embed=em)
		def pred(m):
			return m.author == message.author and m.channel == message.channel
		answer1 = await self.bot.wait_for("message", check=pred)
		if str(answer1.content.lower()) == "y" or str(answer1.content.lower()) == "yes":
			info["current_enemy_name"] = selected_enemy
			fileIO("users/{}/info.json".format(author.id), "save", info)
			enemy_generated_health = random.randint(enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["enemy_min_health"], enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]["enemy_max_health"])
			info["current_enemy_health"] = enemy_generated_health
			fileIO("users/{}/info.json".format(author.id), "save", info)
			em = guilded.Embed(title="{} engages in a fight with {}.".format(info["player_name"], selected_enemy), description="{}'S STATS\nHealth: {}/{}\n\n{}'S STATS\nHealth: {}".format(info["player_name"].upper(), info["player_health"], info["player_max_health"], selected_enemy.upper(), enemy_generated_health), color=0x363942)
			em.set_footer(text="Command ended. Enter the command again.")
			await ctx.send(embed=em)
		elif str(answer1.content.lower()) == "n" or str(answer1.content.lower()) == "no":
			em = guilded.Embed(description="{} continues to wander.".format(info["player_name"]), color=0x363942)
			em.set_footer(text="Command ended. Enter the command again.")
			await ctx.send(embed=em)
		else:
			em = guilded.Embed(description="Invalid input. Returning.", color=0x363942)
			em.set_footer(text="An invalid choice was passed. Enter the command again.")
			await ctx.send(embed=em)
	else:
		selected_enemy = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]
		selected_enemy_name_display = selected_enemy["display_name"]
		em = guilded.Embed(title="{}'s pre-fight information".format(info["player_name"]), description="__**{}**__\n`Health:` {}/{}\n\n__**{}**__\n`Health:` {}".format(info["player_name"], info["player_health"], info["player_max_health"], selected_enemy_name_display, info["current_enemy_health"]), color=0x363942)
		em.set_footer(text="Do you want to FIGHT or ESCAPE? Type one of the key words, no prefix needed.")
		await ctx.send(embed=em)
		def pred(m):
			return m.author == message.author and m.channel == message.channel
		answer1 = await self.bot.wait_for("message", check=pred)
		if str(answer1.content.lower()) == "e" or str(answer1.content.lower()) == "escape":
			num_gen = random.randint(0, 100)
			num_gen = num_gen
			if num_gen < 50:
				enemy_base = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]
				enemy_damage = random.randint(enemy_base["enemy_min_damage"], enemy_base["enemy_max_damage"])
				enemy_damage = enemy_damage
				player_damage = random.randint(weapons[info["player_weapon"]]["min_damage"], weapons[info["player_weapon"]]["max_damage"])
				player_damage = player_damage
				player_health = info["player_health"] - enemy_damage
				enemy_health = info["current_enemy_health"] - player_damage
				em = guilded.Embed(title="{}'s escape information:".format(info["player_name"]), description="{} attacks {} for {} damage as they escape.\n\n`{}'s LOGS`\nDamage taken: {}\nHealth: {}".format(selected_enemy_name_display, info["player_name"], enemy_damage, info["player_name"], enemy_damage, player_health), color=0x363942)
				await ctx.send(embed=em)
				if player_health <= 0:
					info["player_name"] = "None"
					info["player_health"] = 120
					info["player_max_health"] = 120
					info["inventory"] = {
						"silver": 0,
						"recipes": {},
						"items": {},
						"weapons": {},
						"materials": {},
						"locations_unlocked": ["starter area"],
						"healing_items": {}
					}
					info["player_deaths"] += 1
					info["player_enemies_defeated_current_lifetime"] = 0
					info["player_weapon"] = "Fists"
					info["current_enemy_health"] = 0
					info["current_enemy_name"] = "None"
					info["setup"] = "False"
					info["start_command_used"] = "False"
					info["player_armmor"] = "Rags"
					info["player_location"] = "starter area"
					fileIO("users/{}/info.json".format(author.id), "save", info)
					em = guilded.Embed(description="{} has died... Character state reset.".format(author.name), color=0x363942)
					await ctx.send(embed=em)
				else:
					info["player_health"] = player_health
					info["current_enemy_name"] = "None"
					info["current_enemy_health"] = 0
					fileIO("users/{}/info.json".format(author.id), "save", info)
					em = guilded.Embed(description="{}'s escape was successful.".format(info["player_name"]), color=0x363942)
					await ctx.send(embed=em)
			elif num_gen >= 50:
				info["current_enemy_name"] = "None"
				info["current_enemy_health"] = 0
				fileIO("users/{}/info.json".format(author.id), "save", info)
				em = guilded.Embed(description="{}'s escape was successful.".format(info["player_name"]), color=0x363942)
				await ctx.send(embed=em)

		elif str(answer1.content.lower()) == "f" or str(answer1.content.lower()) == "fight":
			enemy_base = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]
			enemy_damage = random.randint(enemy_base["enemy_min_damage"], enemy_base["enemy_max_damage"])
			enemy_damage = enemy_damage
			player_damage = random.randint(weapons[info["player_weapon"]]["min_damage"], weapons[info["player_weapon"]]["max_damage"])
			player_damage = player_damage
			player_max_health = info["player_max_health"]
			player_health = info["player_health"] - enemy_damage
			player_health = player_health
			enemy_health = info["current_enemy_health"] - player_damage
			enemy_health = enemy_health
			if player_health <= 0:
				player_name = info["player_name"]
				selected_enemy_name_display = enemy_base["display_name"]
				info["player_name"] = "None"
				info["player_health"] = 120
				info["player_max_health"] = 120
				info["inventory"] = {
					"silver": 0,
					"recipes": {},
					"items": {},
					"weapons": {},
					"materials": {},
					"locations_unlocked": ["starter area"],
					"healing_items": {}
				}
				info["player_deaths"] += 1
				info["player_enemies_defeated_current_lifetime"] = 0
				info["player_weapon"] = "Fists"
				info["current_enemy_health"] = 0
				info["current_enemy_name"] = "None"
				info["setup"] = "False"
				info["start_command_used"] = "False"
				info["player_armmor"] = "Rags"
				info["player_location"] = "starter area"
				fileIO("users/{}/info.json".format(author.id), "save", info)
				em = guilded.Embed(title="{} engages in a fight with {}".format(player_name, selected_enemy_name_display), description="`{}'S LOGS`\nDamage taken: {}\nHealth: {}/{}\n\n`{}'S LOGS`\nDamage taken: {}\nHealth: {}".format(player_name.upper(), enemy_damage, player_health, player_max_health, selected_enemy_name_display.upper(), player_damage, enemy_health), color=0x363942)
				await ctx.send(embed=em)
				em = guilded.Embed(description="{} has died... Character state reset.".format(author.name), color=0x363942)
				await ctx.send(embed=em)
			else:
				if enemy_health <= 0:
					enemy_base = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]
					enemy_damage = random.randint(enemy_base["enemy_min_damage"], enemy_base["enemy_max_damage"])
					enemy_damage = enemy_damage
					player_damage = random.randint(weapons[info["player_weapon"]]["min_damage"], weapons[info["player_weapon"]]["max_damage"])
					player_damage = player_damage
					player_max_health = info["player_max_health"]
					player_health = info["player_health"] - enemy_damage
					enemy_health = info["current_enemy_health"] - player_damage
					em = guilded.Embed(title="{} engages in a fight with {}".format(info["player_name"], selected_enemy_name_display), description="`{}'S LOGS`\nDamage taken: {}\nHealth: {}/{}\n\n`{}'S LOGS`\nDamage taken: {}\nHealth: {}".format(info["player_name"].upper(), enemy_damage, player_health, player_max_health, selected_enemy_name_display.upper(), player_damage, enemy_health), color=0x363942)
					await ctx.send(embed=em)
					info["player_enemies_defeated_current_lifetime"] += 1
					info["player_enemies_defeated"] += 1
					info["current_enemy_name"] = "None"
					info["current_enemy_health"] = 0
					info["player_health"] = info["player_health"] - enemy_damage
					fileIO("users/{}/info.json".format(author.id), "save", info)
					em = guilded.Embed(title="Enemy defeated.", description="{} has died...".format(selected_enemy_name_display), color=0x363942)
					await ctx.send(embed=em)
				else:
					enemy_base = enemies["locations"][info["player_location"]]["enemies"][info["current_enemy_name"]]
					enemy_damage = random.randint(enemy_base["enemy_min_damage"], enemy_base["enemy_max_damage"])
					enemy_damage = enemy_damage
					player_damage = random.randint(weapons[info["player_weapon"]]["min_damage"], weapons[info["player_weapon"]]["max_damage"])
					player_damage = player_damage
					player_max_health = info["player_max_health"]
					player_health = info["player_health"] - enemy_damage
					enemy_health = info["current_enemy_health"] - player_damage
					info["player_health"] = info["player_health"] - enemy_damage
					info["current_enemy_health"] = info["current_enemy_health"] - player_damage
					fileIO("users/{}/info.json".format(author.id), "save", info)
					em = guilded.Embed(title="{} engages in a fight with {}".format(info["player_name"], selected_enemy_name_display), description="`{}'S LOGS`\nDamage taken: {}\nHealth: {}/{}\n\n`{}'S LOGS`\nDamage taken: {}\nHealth: {}".format(info["player_name"].upper(), enemy_damage, player_health, player_max_health, selected_enemy_name_display.upper(), player_damage, enemy_health), color=0x363942)
					em.set_footer(text="Type the command again to continue.")
					await ctx.send(embed=em)
		else:
			em = guilded.Embed(description="An invalid choice was passed. Enter the command again.", color=0x363942)
			em.set_footer(text="Choices: F, Fight | OR | E, Escape")
			await ctx.send(embed=em)

def setup(bot):
	bot.add_cog(Rep(bot))