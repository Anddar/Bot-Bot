# All the imported packages needed to run this cog.
import discord
from discord.ext import commands
import os, sys

class Restart(commands.Cog):

		def __init__(self, bot):
				self.bot = bot

		# Events


		# Commands
		@commands.command(help = "The ?restart command will execute a full kernel restart of the bot allowing for the fix of persistent errors.", pass_context = True, aliases = [])
		async def restart(self, ctx):
				# Telling user the bot has been restarted 
				await ctx.channel.send("```The Bot is restarting...be back momentarily. Wait ~ 30 Seconds```")

				sys.stdout.flush()
				os.execv(sys.argv[0], sys.argv)

def setup(bot):
		bot.add_cog(Restart(bot))