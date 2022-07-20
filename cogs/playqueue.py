# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

from math import ceil

from multiprocessing.pool import ThreadPool
import os
import shutil

import sys
sys.path.insert(0, '/home/ubuntu/Bot-Bot') # So we can import downloads

import asyncio
from downloads import downloadSong, downloadSongQ, getSongData

class PlaySong(commands.Cog):

		def __init__(self, bot):
				self.bot = bot
				self.queues = {}
				self.q_num = {}
				self.queue_list = {}
				self.servers = {}
				self.loops = {}
				self.loopTimes = {}

		# Events
		

		# Commands

		@commands.command(help = "The command ?play or ?p will play as song if given a youtube link or song name with the artist. If a song is already playing it will add it to the queue", pass_context = True, aliases = ['p'])
		async def play(self, ctx):

				def check_queue():

						if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue"):
								if self.loops[ctx.guild.id] == "loopConstant":
										shutil.copyfile(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3", f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song0.mp3")
								
								elif self.loops[ctx.guild.id] == "loopAmount" and self.loopTimes[ctx.guild.id] > 0:
										shutil.copyfile(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3", f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song0.mp3")
										self.loopTimes[ctx.guild.id] -= 1

								elif self.loopTimes[ctx.guild.id] == 0:
										self.loops[ctx.guild.id] = "noLoop"

								DIR = f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue"
								length = len(os.listdir(DIR))

								try:
										if self.loops[ctx.guild.id] == "loopAmount" or self.loops[ctx.guild.id] == "loopConstant":
												first_file = "song0.mp3"
										else:
												first_file = "song1.mp3"
								except Exception:
										print("Queue list is empty...")
										self.queues[ctx.guild.id].clear()
										return

								main_location = f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}"
								song_path = f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/" + first_file

								# If there are songs in the queue file then we want to remove the old song from the main directory and move the top song in the Queue directory to be played from the main area.
								if length != 0:
										if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3"):
												os.remove(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3")
										shutil.move(song_path, main_location)

										if self.loops[ctx.guild.id] == "noLoop":
												# Pop the song that was moved to be played out of our queue list
												self.queue_list[ctx.guild.id].pop(1)
									
												# Queue should be shifted down 1 since we took the top song out of the queue
												self.queues[ctx.guild.id].pop(self.q_num[ctx.guild.id])
												self.q_num[ctx.guild.id] -= 1
									
												# Lower each songs name and position number by 1.
												for i in range(2, self.q_num[ctx.guild.id]+2):
														if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song{i}.mp3"):
																os.rename(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song{i}.mp3", f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song{i-1}.mp3")

										for file in os.listdir(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}'):
												if file.endswith(".mp3"):
														os.rename(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/{str(first_file)}", f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3")

										# Play the song the was moved to the main directory.
										os.chmod(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3', 0o777)
										voice.play(discord.FFmpegPCMAudio(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3'), after=lambda e: check_queue())
										voice.source = discord.PCMVolumeTransformer(voice.source)
										voice.source.volume = 0.07

								# If there are no more songs in the queue then we can clear this servers queue dictionary.
								else:
										self.queues[ctx.guild.id].clear()
										return

						# If the queue folder doesn't exist then we clear the queue and finish check_queue.
						else:
								self.queues[ctx.guild.id].clear()
				
				# Get the discord servers id
				self.servers[ctx.guild.id] = str(ctx.guild.id)

				# Make server file if it doesn't exist
				if not os.path.exists(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}'):
						os.mkdir(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}")
						os.chmod(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}", 0o777)
						await asyncio.sleep(2)
						os.mkdir(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong")
						os.chmod(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong", 0o777)

				# Get the contents of the message sent to the bot
				songInfo = ctx.message.content
				if songInfo.startswith("?play"):
						songInfo = ((songInfo).lstrip('?play')).strip()
				elif songInfo.startswith("?p"):
						songInfo = ((songInfo).lstrip('?p')).strip()

				# Getting the current state of the bots voice as well as the channel that the user is in.
				voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
				channel = str(ctx.author.voice.channel)

				# Make sure the user is in a voice channel and that actual song info was given
				if songInfo == "":
						await ctx.channel.send("```You must provide a link or song name to play a song.```")
						return	
					
				elif ctx.author.voice == None:
						await ctx.channel.send("```You must be inside of a voice channel to play music or inside the same voice channel as the bot.```")
						return			

				# If the bot is currently playing a song we want to queue it and if its not in a channel we want it to join.
				if voice != None:
						if voice.is_playing():
								await self.queue(ctx)
								return
				else:
						Basic = self.bot.get_cog('Basics')
						await Basic.join(ctx)

				voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) # Get the voice client after it joins

				# Make sure user and bot are in same channel if a command is given.
				if channel != str(voice.channel):
						await ctx.channel.send("```You must be in the same voice channel as the bot to request a song to be played.```")
						return

				# Deleting all old song files within the main server folder, setupsong folder and get rid of all old queue folders including its contents.
				for file in os.listdir(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/'):
						if str(file) != ".spotdl-cache" and str(file) != "SetupSong" and str(file) != "Queue":
								os.remove(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/{str(file)}')

				for file in os.listdir(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong/'):
						if str(file) != ".spotdl-cache":
								os.remove(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong/{str(file)}')

				if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue"):
						shutil.rmtree(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue")
			
				self.queues[ctx.guild.id] = {}
				self.q_num[ctx.guild.id] = 0
				self.queue_list[ctx.guild.id] = ["loopReserve"]
				self.loops[ctx.guild.id] = "noLoop"
				self.loopTimes[ctx.guild.id] = 0

				# Downloading the song requested
				pool = ThreadPool(processes=1)
				async_result = pool.apply_async(downloadSong, (songInfo, self.servers[ctx.guild.id]))
				vid = async_result.get() # Get the return value from our function.

				#await asyncio.sleep(2)
			
				# Playing the song that was requested
				os.chmod(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3', 0o777)
				try:
					voice.play(discord.FFmpegPCMAudio(f'/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/song.mp3'), after=lambda e: check_queue())
					voice.source = discord.PCMVolumeTransformer(voice.source)
					voice.source.volume = 0.07
				except Exception as e:
					print(e)

				# Creating the embeded message from our youtube object that was returned when downloading the song.
				pool = ThreadPool(processes=1)
				async_result = pool.apply_async(getSongData, (vid, ctx))
				embed = async_result.get()  # Get the return value from your function.

				# Try to send the embeded message and add all reactions.
				try:
						msg = await ctx.channel.send(embed=embed)
						await msg.add_reaction("⏯")
						await msg.add_reaction("⏭")
						await msg.add_reaction("⏹")
						await msg.add_reaction("🔁")
						await msg.add_reaction("🔂")
				except:
						await ctx.channel.send("```Now Playing: Song (Error Retrieving Song Information)```")

				return

		@commands.command(help = "The command ?queue or ?q will add a song to the queue of songs to be played.", pass_context = True, aliases = ['q', 'que'])
		async def queue(self, ctx):

				# Get the current status of the bots voice client
				voice = discord.utils.get(self.bot.voice_clients, guild = ctx.guild)

				# Retrieve the information that the user gave
				songInfo = ctx.message.content
				if songInfo.startswith("?queue"):
						songInfo = ((ctx.message.content).lstrip('?queue')).strip()
				elif songInfo.startswith("?q"):
						songInfo = ((ctx.message.content).lstrip('?q')).strip()
				elif songInfo.startswith("?que"):
						songInfo = ((ctx.message.content).lstrip('?que')).strip()
				elif songInfo.startswith("?play"):
						songInfo = ((ctx.message.content).lstrip('?play')).strip()
				elif songInfo.startswith("?p"):
						songInfo = ((ctx.message.content).lstrip('?p')).strip()

				# Make sure the bot is playing music before trying to queue a song.
				if voice == None or (not voice.is_playing()):
						await ctx.channel.send("```The bot needs to be playing music and connected to a channel before you can start queuing songs for it to play.```")
						return

				elif songInfo == "":
						await ctx.channel.send("```You must provide a link or song name to play a song.```")
						return

				elif str(ctx.author.voice.channel) != str(voice.channel):
						await ctx.channel.send("```You must be in the same voice channel as the bot to queue a song to be played.```")
						return

				# If the queue does not exist then we need to make a folder to hold all queued songs.
				if not os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue"):
						os.mkdir(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue")
						os.chmod(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue", 0o777)
						for file in os.listdir(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong"):
								os.remove(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong/{str(file)}")
				
				DIR = f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue"

				self.q_num[ctx.guild.id] = len(os.listdir(DIR))
				self.q_num[ctx.guild.id] += 1

				add_Queue = True
				while add_Queue:
						if self.q_num[ctx.guild.id] in self.queues[ctx.guild.id]:
								self.q_num[ctx.guild.id] += 1
						else:
								add_Queue = False
								(self.queues[ctx.guild.id])[self.q_num[ctx.guild.id]] = self.q_num[ctx.guild.id]

				print("Queue Num: ", self.q_num[ctx.guild.id], "Queues: ", self.queues[ctx.guild.id])
							
				# Downloading the requested song into the queue
				pool = ThreadPool(processes=1)
				async_result = pool.apply_async(downloadSongQ, (songInfo, self.q_num[ctx.guild.id], self.servers[ctx.guild.id])) 
				vid = async_result.get() # Get the return value from our function.
			
				# Add the downloaded song to our queue list of songs
				self.queue_list[ctx.guild.id].append(str(vid.title) + " " + str(vid.author))
				
				#await asyncio.sleep(2)

				# Creating the embeded message from our youtube object that was returned when downloading the song.
				pool = ThreadPool(processes=1)
				async_result = pool.apply_async(getSongData, (vid, ctx, self.q_num[ctx.guild.id], True))
				embed = async_result.get() # Get the return value from our function.
			
				# Try to send the embeded message and add all reactions.
				try:
						msg = await ctx.channel.send(embed=embed)
						await msg.add_reaction("⏯")
						await msg.add_reaction("⏭")
						await msg.add_reaction("⏹")
						await msg.add_reaction("🔁")
						await msg.add_reaction("🔂")
				except:
						await ctx.channel.send("```Queuing Song: Song (Error Retrieving Song Info)```")

				return

		@commands.command(help = "The command ?clearq or ?cq will clear the queue of songs.", pass_context = True, aliases = ['cq'])
		async def clearq(self, ctx):
				if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue"):
						shutil.rmtree(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue")

				if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong"):
						for file in os.listdir(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong"):
								os.remove(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/SetupSong/{str(file)}")

				self.queues[ctx.guild.id].clear() # Clear the queue dictionary.
				self.queue_list[ctx.guild.id] = ["loopReserve"]

				# Tell user that the queue was cleared for them.
				await ctx.channel.send("```Queue has been cleared.```")

				return

		@commands.command(help = "The command ?removeq or ?rq will remove a song in the queue based on its position in the queue. This position can be found by the 'Queuing Song' print out in the bottom right.", pass_context = True, aliases = ['rq'])
		async def removeq(self, ctx):
				serverID = ctx.guild.id
				
				if ctx.message.content.startswith('?removeq'):
						position = ((ctx.message.content).lstrip('?removeq')).strip()
				else:
						position = ((ctx.message.content).lstrip('?rq')).strip()

				if not os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{serverID}/Queue/song{position}.mp3"):
						await ctx.channel.send(f"```No song was found at that position in the queue or the input given was invalid and could not be understood.```")
						return
				elif not position.isdigit():
						await ctx.channel.send(f"```The position value given was not an integer please pass the integer position of the song to remove the song.```")
						return

				position = int(position) # Turn position into an integer

				if len(self.queues[serverID]) >= 1:
						try:
								os.remove(f"/home/ubuntu/Bot-Bot/servers/main{serverID}/Queue/song{position}.mp3")

								# Pop the song out of our queue list
								(self.queue_list[ctx.guild.id]).pop(position)
							
								# Subtract queue by 1 and lower all the position numbers of the songs until the position given by the user
								self.queues[ctx.guild.id].pop(self.q_num[ctx.guild.id])
								self.q_num[ctx.guild.id] -= 1

								for i in range(position+1, self.q_num[ctx.guild.id]+2):
										if os.path.exists(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song{i}.mp3"):
												os.rename(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song{i}.mp3", f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.guild.id]}/Queue/song{i-1}.mp3")

								await ctx.channel.send(f"```The song at position {position} in the queue has been successfully removed.```")

						except Exception as e:
								print(e)

						return

				else:
						await ctx.channel.send(f"```There is no queue, cannot remove song at position {position}.```")
						return

				return

		@commands.command(help = "The ?loop command will loop a song until ?loop is executed again then looping will stop.", pass_context = True, aliases = ["loop1"])
		async def loop(self, ctx):

				if str(ctx) != "🔁" and str(ctx) != "🔂":
						voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
						if voice != None:
								if not voice.is_playing():
									await ctx.message.channel.send("```Cannot loop a song if the bot is not playing a song.```")
									return
						elif voice == None:
								await ctx.message.channel.send("```Bot is not connected to a voice channel cannot loop song.```")
								return
				
				if str(ctx) == "🔁" or str(ctx.message.content).strip() == "?loop":
						if self.loops[ctx.message.guild.id] == "loopConstant":
								self.loops[ctx.message.guild.id] = "noLoop"
								await ctx.message.channel.send("```Constant loop of the current song has stopped.```")
								return
								
						self.loops[ctx.message.guild.id] = "loopConstant"

				elif str(ctx) == "🔂" or str(ctx.message.content).strip() == "?loop1":
						if self.loops[ctx.message.guild.id] == "loopAmount":
								self.loops[ctx.message.guild.id] = "noLoop"
								await ctx.message.channel.send("```You have stopped the loop of the song early.```")
								return
								
						self.loops[ctx.message.guild.id] = "loopAmount"
						self.loopTimes[ctx.message.guild.id] = 1

				else:
						await ctx.message.channel.send("```Loop command given was not understood use ?help for more information on the bots commands.```")
						return
			
				if len(self.queues[ctx.message.guild.id]) == 0:
						os.mkdir(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.message.guild.id]}/Queue/")
						os.chmod(f"/home/ubuntu/Bot-Bot/servers/main{self.servers[ctx.message.guild.id]}/Queue", 0o777)
						self.q_num[ctx.message.guild.id] = 1
						(self.queues[ctx.message.guild.id])[self.q_num[ctx.message.guild.id]] = self.q_num[ctx.message.guild.id]
			
				await ctx.message.channel.send("```Song will now start looping.```")

				return


		@commands.command(help = "The command ?qlist or ?ql will give the current list of songs in the queue and their positions.", pass_context = True, aliases = ['ql'])
		async def qlist(self, ctx):
				if ctx.message.content.startswith('?qlist'):
						page = ((ctx.message.content).lstrip('?qlist')).strip()
				else:
						page = ((ctx.message.content).lstrip('?ql')).strip()

				if ctx.guild.id in self.queue_list:
						if len(self.queue_list[ctx.guild.id]) <= 1:
								await ctx.channel.send("```There are currently no songs in the queue cannot print the queue list.```")
								return
						elif page == None or page == "":
								page = 1
						elif page.isdigit():
								try:
									page = int(page)
								except:
									page = 1
						else:
								await ctx.channel.send("```Improper page number given please specify a integer page number to show the queue list.```")
								return
				else:
						await ctx.channel.send("```There is currently no song playing so there is no possible way for there to be a queue list.```")
						return

				totalPages = ceil(len(self.queue_list[ctx.guild.id])/10)
				if page > totalPages:
						await ctx.channel.send("```QueueList page number entered is out of range, page does not exist as there are not enough songs in queue to reach that page.```")
						return
					
				# Finding the starting page number
				if page > 1:
						start_page = 10*(page-1) + 1
				else:				
						start_page = 1
					
				# Calculate the end page number
				if start_page != 1:	
					end_page = ((len(self.queue_list[ctx.guild.id])) - start_page) + 10*(page-1)
					
				else:
						if len(self.queue_list[ctx.guild.id]) >= 11:
								end_page = 10
						else:
								end_page = len(self.queue_list[ctx.guild.id])-1
							
				# Creating the embeded queue list to print out in the discord text channel.
				qlist_embed = discord.Embed(title=f"QueueList: Page {page}", description=f"This is the list of songs currently in the queue from position {start_page} to {end_page}.", color=discord.Color.dark_blue())
				for i in range(start_page, end_page+1):
						if len(self.queue_list[ctx.guild.id][i]) >= 50:
								qlist_embed.add_field(name=f'Pos. {i}', value=self.queue_list[ctx.guild.id][i][0:49] + "...")
						else:
								qlist_embed.add_field(name=f'Pos. {i}', value=str(self.queue_list[ctx.guild.id][i]))

				if totalPages - page > 0:
						qlist_embed.set_footer(text=f"Page {page} of {ceil(len(self.queue_list[ctx.guild.id])/10)}. Use ?qlist {page+1} or ?ql {page+1} to see the next page.")
				else:
						qlist_embed.set_footer(text=f"Page {page} of {ceil(len(self.queue_list[ctx.guild.id])/10)}.")
				
				await ctx.channel.send(embed=qlist_embed)
				
def setup(bot):
		bot.add_cog(PlaySong(bot))