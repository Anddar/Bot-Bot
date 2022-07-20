# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

class StartJoin(commands.Cog):

		def __init__(self, bot):
				self.bot = bot

	# Events

		# This event just prints to console when the bot has started and logged in to Discord.
		@commands.Cog.listener()
		async def on_ready(self):
				print('We have logged in as {0.user}'.format(self.bot))

		@commands.Cog.listener()
		async def on_guild_join(self, guild):
				decider = False

				for channel in guild.text_channels:

						channelName = str(channel)

						if ('general' in channelName) and (channel.permissions_for(
		guild.me).send_messages):

								await channel.send('```Hi, I am Bot Bot and I am mainly a music bot, shhh dont tell Youtube, but I can do some other cool tasks. Use ?help to get see what I can do.```')

								decider = True

								return

				if decider == False:

						for channel in guild.text_channels:

								if (channel.permissions_for(guild.me).send_messages):

										await channel.send('```Hi, I am Bot Bot and I am mainly a music bot, shhh dont tell Youtube, but I can do some other cool tasks. Use ?help to see what I can do.```')

										return

	# Commands


def setup(bot):
		bot.add_cog(StartJoin(bot))