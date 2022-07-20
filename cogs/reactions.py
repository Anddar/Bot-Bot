# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

class Reactions(commands.Cog):
		
		def __init__(self, bot):
				self.bot = bot

		# Events

		@commands.Cog.listener()
		async def on_reaction_add(self, Reaction, user):
				if str(user) == "Bot Bot#7012":
						return
				
				# Getting access to the voice client 
				voice = discord.utils.get(self.bot.voice_clients, guild = user.guild)

				if str(user.voice.channel) != str(voice.channel):
						await Reaction.message.channel.send("```You must be in the same channel as the bot to execute reaction commands.```")
						return

				Basics = self.bot.get_cog('Basics')
				PlaySong = self.bot.get_cog('PlaySong')

				if str(Reaction) == "⏯":
						if voice != None:
								if voice.is_paused():
										await Basics.resume(Reaction.message)
										return
								else:
										await Basics.pause(Reaction.message)
										return
				elif str(Reaction) == "⏭":
						await Basics.skip(Reaction.message)
						return
				elif str(Reaction) == "⏹":
						await Basics.stop(Reaction.message)
						return
				elif str(Reaction) == "🔁":
						await PlaySong.loop(Reaction)
						return
				elif str(Reaction) == "🔂":
						await PlaySong.loop(Reaction)
						return
				else:
						return

				return

		# Commands

def setup(bot):
		bot.add_cog(Reactions(bot))