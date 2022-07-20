# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

class Basics(commands.Cog):

		def __init__(self, bot):
				self.bot = bot

		# Events


		# Commands

		@commands.command(help = "The command ?join or ?j will make the bot join the voice channel you are in.", pass_context = True, aliases = ['j'])
		async def join(self, ctx):
				# Aquiring the voice clients for the bot as well as what channel the the user who sent the join command was in.
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)
				channel = ctx.author.voice.channel
			
				# If the voice is None that means that bot is not connected to a channel and so we can tell the bot to connect to the channel that the user who set the command is in.
				if (voice == None) or (not voice.is_connected()):
						await ctx.channel.send(f"```The bot has joined {ctx.author.voice.channel} channel.```")
						await channel.connect()
						return

				# If voice is not None meaning that is may be already in a channel.
				elif voice != None:
						# If the voice is not playing then the bot should be allowed to connect to the channel that the new user is calling it from.
						if not voice.is_playing():
								PlaySong = self.bot.get_cog('PlaySong')

								await PlaySong.clearq(ctx) # clear the queue just incase there are songs needed to be played
								await voice.disconnect()
								await channel.connect()
								await ctx.channel.send(f"```The bot has moved to the {ctx.author.voice.channel} channel.```")
								return
						else: # Besides that if the bot is playing we give the user a message
								await ctx.channel.send("```I believe that I am already in a channel playing music. Connect to that channel to play music.```")
								return


		@commands.command(help = "The command ?leave or ?l will ask the bot to leave the channel.", pass_context = True, aliases = ['l'])
		async def leave(self, ctx):
				# Getting access to the voice client
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

				# If the voice is not none meaning we are in a voice channel
				if voice != None:
						# Making sure the voice is 100% conncected then:
						if voice.is_connected():
								# Tell the user what channel the bot has left from and disconnect the bot.
								await ctx.channel.send(f"```The bot has left {voice.channel} voice channel.```")

								PlaySong = self.bot.get_cog('PlaySong')
								await PlaySong.clearq(ctx)

								if voice.is_playing():
									voice.stop()
								await voice.disconnect()
								return

				else: # If the bot is not connected to a channel it can't leave.
						await ctx.channel.send("```The bot is not connected to a voice channel so it cannot leave.```")
						return


		@commands.command(help = "The command ?pause will pause the music being played at the moment.", pass_context = True, aliases = [])
		async def pause(self, ctx):

				# Getting access to the bots voice client.
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

				if str(ctx.author.voice.channel) != str(voice.channel):
						await ctx.channel.send("```You must be in the same channel as the bot to pause the bot's music.```")
						return

				# Checking if voice is not none meaning it is connected to a voice channel.
				if voice != None:
						# We make sure that the voice is playing before attempting to pause audio.
						if voice.is_playing():
								# Telling user the audio was paused
								await ctx.channel.send("```Audio being paused...```")
								voice.pause()
								return
						else: # If there is no audio playing we can't pause the audio.
								await ctx.channel.send("```No audio is playing cannot pause.```")
								return 

				else: # If there is no audio or bot is not connected to a voice channel then we need to account for these errors.
						await ctx.channel.send("```No audio is playing or is not connected to a voice channel so we cannot pause.```")
						return
			

		@commands.command(help = "The command ?resume or ?r will resume the music from where it was paused.", pass_context = True, aliases = ['r'])
		async def resume(self, ctx):
				# Getting access to the bots voice clients.
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

				if str(ctx.author.voice.channel) != str(voice.channel):
						await ctx.channel.send("```You must be in the same channel as the bot to resume the bot's music.```")
						return

				# If voice is not none meaning that we are in a voice channel.
				if voice != None:
						# If the audio is paused then and only then we can resume audio
						if voice.is_paused():
								# Tell user that audio is being resumed.
								await ctx.channel.send("```Audio being resumed...```")
								voice.resume()
								return

						else: # If the audio is not paused then we can't resume audio.
								await ctx.channel.send("```The audio is not paused so we cannot resume.```")
								return

				else: # If the audio is not paused or if the bot is not connected to a voice channel then we need to account for these errors.
						await ctx.channel.send("```The audio is not paused or we are not connected to a voice channel so we cannot resume.```")
						return

		@commands.command(help = "The command ?skip or ?s will skip to the next song in the queue.", pass_context = True, aliases = ['s'])
		async def skip(self, ctx):
				# Getting access to the voice client 
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

				if str(ctx.author.voice.channel) != str(voice.channel):
						await ctx.channel.send("```You must be in the same channel as the bot to skip the current song.```")
						return

				# Checking if voice is not none meaning that it is in a voice channel and if the bot is playing then we can skip a song.
				if voice != None:
						if voice.is_playing():
								PlaySong = self.bot.get_cog('PlaySong')
								if len(PlaySong.queue_list[ctx.guild.id]) > 1:
									await ctx.channel.send(f"```Now Playing {PlaySong.queue_list[ctx.guild.id][1]}...```")
								else:
									await ctx.channel.send(f"```No next song to skip to. Use ?p or ?play to play the next song```")
								voice.stop() # Doing voice stop will actually skip to the next song
								return

						else: # User cannot skip to next song if nothing is playing.
								await ctx.channel.send("```No music playing cannot skip to next song.```")
								return

				return

		@commands.command(help = "The ?stop command will stop all music from being played clear the queue and ask the bot to leave the voice channel.", pass_context = True, aliases = [])
		async def stop(self, ctx):
				# Getting access to the bots voice clients.
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

				# If voice is not none meaning that we are connected to a voice channel then we are allowed to stop the bot.
				if voice != None:
						# Telling the user we have stopped the bot and everything that will happen from stopping it.
						await ctx.channel.send("```The bot has been stopped and will terminate all music, queues and leave the channel.```")
						
						PlaySong = self.bot.get_cog('PlaySong')
						await PlaySong.clearq(ctx) # Making sure to clear queue before stopping.
						if voice.is_playing():
							voice.stop() # Stopping
						await voice.disconnect() # Disconnecting
						return

				else: # If the bot is not connected to a channel or doing anything we can't stop the bot.
						await ctx.channel.send("```Bot not connected to voice channel, cannot be stopped.```")
						return

def setup(bot):
		bot.add_cog(Basics(bot))