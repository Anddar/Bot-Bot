# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

class Error(commands.Cog):

		def __init__(self, bot):
				self.bot = bot

		# Events

		@commands.Cog.listener()
		async def on_command_error(self, ctx, error):

				# Handles if the user gives a command that is not understood by the bot and tells user where they can find the useable commands.
				if isinstance(error, commands.CommandNotFound):
						await ctx.channel.send("```The command you have entered was not found in the bots list of understood commands. Use ?help to see all the of the bots commands.```")

		# Commands

def setup(bot):
		bot.add_cog(Error(bot))