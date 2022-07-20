import discord
from discord.ext import commands

import asyncio

class AFKLeave(commands.Cog):

		def __init__(self, bot):
				self.bot = bot
		
		# Events

		@commands.Cog.listener()
		async def on_voice_state_update(self, member, before, after):
    
				if not member.id == self.bot.user.id:
						return

				elif before.channel is None:
						voice = after.channel.guild.voice_client
						time = 0
						while True:
								await asyncio.sleep(1)
								time = time + 1
								if voice.is_playing() and not voice.is_paused():
										time = 0
								if time == 300:
										await voice.disconnect()
								if not voice.is_connected():
										break
		
		# Commands

def setup(bot):
		bot.add_cog(AFKLeave(bot))