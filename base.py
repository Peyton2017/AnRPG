import guilded
from guilded.ext import commands
import random
import json
import glob
import os
from tools.dataIO import fileIO
from core import checks

with open('config/config.json') as f:
    config = json.load(f)

token = config["Token"]
cogs = [os.path.basename(f) for f in glob.glob("modules/*.py")]
startup = ["modules." + os.path.splitext(f)[0] for f in cogs]
bot = commands.Bot(bot_id="8f16b207-3de1-4167-aeca-8d3f9b6c90f0",command_prefix=".")

@bot.event
async def on_ready():
    print("Online!")
    print('------')

@bot.command()
@checks.is_dev()
async def load(ctx, *, cog_name: str):
    if not cog_name.startswith("modules."):
        cog_name = "modules." + cog_name
    try:
        bot.load_extension(cog_name)
    except Exception as e:
        em = guilded.Embed(description="Failed to load the Module.", color=0x363942)
        await ctx.send(embed=em)
        print('{}: {}'.format(type(e), e))
    else:
        em = guilded.Embed(description="**Module loaded.** :)", color=0x363942)
        await ctx.send(embed=em)

@bot.command()
@checks.is_dev()
async def unload(ctx, *, cog_name: str):
    if not cog_name.startswith("modules."):
        cog_name = "modules." + cog_name

    if cog_name in bot.extensions:
        bot.unload_extension(cog_name)
        em = guilded.Embed(description="**Module unloaded.** :)", color=0x363942)
        await ctx.send(embed=em)
    else:
        em = guilded.Embed(description="That Module isn't loaded.", color=0x363942)
        await ctx.send(embed=em)

@bot.command(name="reload")
@checks.is_dev()
async def _reload(ctx, *, cog_name: str):
    if not cog_name.startswith("modules."):
        cog_name = "modules." + cog_name
    try:
        bot.unload_extension(cog_name)
        bot.load_extension(cog_name)
    except Exception as e:
        em = guilded.Embed(description="Failed to reload the Module.", color=0x363942)
        await ctx.send(embed=em)
        print('{}: {}'.format(type(e), e))
    else:
        em = guilded.Embed(description="**Module reloaded.** :)", color=0x363942)
        await ctx.send(embed=em)

if __name__ == '__main__':
    for thing in startup:
        bot.load_extension(thing)
    bot.run(token)