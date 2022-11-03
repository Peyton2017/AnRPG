import guilded
from guilded.ext import commands
from tools.dataIO import fileIO
	
def is_dev_check(ctx):
	config = fileIO("config/config.json", "load")
	if str(ctx.message.author_id) in config["Developer"]:
		return True
	else:
		return False      
		
def is_dev():
	return commands.check(is_dev_check)