# All the imported packages needed to run the bot.
import discord
from discord.ext import commands
import os
from decouple import config

try:
		embedHelp = discord.Embed(title="Help Command List:", description="You can also do ?help [commandname] for help on a specific command.", color=discord.Color.dark_blue())
		embedHelp.add_field(name='?play | ?p', value="The command ?play or ?p will play as song if given a youtube link or song name with the artist. If a song is already playing it will add it to the queue", inline = True)
		embedHelp.add_field(name='?queue | ?que | ?q', value="The command ?queue or ?q will add a song to the queue of songs to be played.", inline = True)
		embedHelp.add_field(name='?qlist | ?ql', value="The command ?qlist or ?ql will print a embed message that contains 10 queued songs per page and their current positions.")
		embedHelp.add_field(name='?clearq | ?cq', value="The command ?clearq or ?cq will clear the queue of songs.", inline = True)
		embedHelp.add_field(name='?removeq | ?rq', value="The command ?removeq or ?rq will remove a song in the queue based on its position in the queue. This position can be found by using the command ?qlist or ?ql to see the position of all current songs in the queue.", inline = True)
		embedHelp.add_field(name='?loop | ?loop1', value="The commands ?loop and ?loop1 will both loop the current song playing except ?loop will loop indefinitely and ?loop1 will loop the song once then resume the queue songs. If you ever want to cancel the looping of a song just send the command ?loop or ?loop1 again and the loop will stop.")
		embedHelp.add_field(name='?join | ?j', value="The command ?join or ?j will make the bot join the voice channel you are in.", inline = True)
		embedHelp.add_field(name='?leave | ?l', value="The command ?leave or ?l will ask the bot to leave the channel.", inline = True)
		embedHelp.add_field(name='?pause', value="The command ?pause will pause the music being played at the moment.", inline = True)
		embedHelp.add_field(name='?resume | ?r', value="The command ?resume or ?r will resume the music from where it was paused.", inline = True)
		embedHelp.add_field(name='?skip | ?s', value="The command ?skip or ?s will skip to the next song in the queue.", inline = True)
		embedHelp.add_field(name='?stop', value="The ?stop command will stop all music from being played clear the queue and ask the bot to leave the voice channel.", inline = True)
		embedHelp.add_field(name='?restart', value="The ?restart command will execute a full kernel restart of the bot allowing for the fix of persistent errors.", inline = True)
		embedHelp.add_field(name='?valorant | ?val | ?v', value="The command ?v will choose a random Agent to play as in Valorant.", inline = True)
		embedHelp.add_field(name='?overwatch | ?ow | ?o', value="The command ?o will choose a random Hero to play as in Overwatch.", inline = True)
		embedHelp.add_field(name='?ov', value="The command ?ov will choose a random Hero to play as in Overwatch and a random Agent to play in Valorant.", inline = True)		

		embedPlay = discord.Embed(title = "?play | ?p", description = "This command will play a song. The requirements are a Youtube Link, or a Spotify Link, or a song name of the format '?play artist songName' for the best search criteria. If there is a song currently playing and this command is executed it will hand the song over to the queue and add it to the end of the queue.", color=discord.Color.dark_blue())		

		embedQueue = discord.Embed(title = "?queue | ?que | ?q", description="This command will queue a song. The requirements for this command are also a Youtube Link, or a Spotify Link, or a song name of the format '?queue artist songName' for the best search criteria.", color=discord.Color.dark_blue())

		embedQueueList = discord.Embed(title = "?qlist | ?ql | ?q", description="The command ?qlist or ?ql will print a embed message that contains 10 queued songs per page and their current positions this can be used to help with removing a specific song in the queue with ?removeq or rq. Use ?qlist 2 or ?ql 2 to go to next page if it exists.", color=discord.Color.dark_blue())

		embedClearQ = discord.Embed(title = "?clearq | ?cq", description="This command will clear the current queue of the bot in your server. This command requires no additional arguments to work all you have to do is '?clearq' or '?cq' and the current queue will be cleared.", color=discord.Color.dark_blue())

		embedRemoveQ = discord.Embed(title = "?removeq | ?rq", description="This command will remove a song at a specified position/location in the queue. The requirements of this command is the position of the song you wish to remove from the queue and can be used like this, Example: '?removeq 1' removed song a position one in the queue. If given an invalid queue position the bot will not remove anything from the queue. These queue  positions can be found by using ?qlist or ?ql to see a list of songs and their positions in the queue.", color=discord.Color.dark_blue())

		embedLoop = discord.Embed(title = "?loop | ?loop1", description="The commands ?loop and ?loop1 will both loop the current song playing except ?loop will loop indefinitely and ?loop1 will loop the song once then resume the queue songs. If you ever want to cancel the looping of a song just send the command ?loop or ?loop1 again and the loop will stop.", color=discord.Color.dark_blue())

		embedJoin = discord.Embed(title = "?join | ?j", description="This command will tell the bot to join the voice channel that you are currently in. Cannot be used if you are not currently in a voice channel. If you would like to have the bot move to a different channel and it is not playing music at the moment this command is sufficent to have the bot move to that voice channel. There are no additional arguements needed for this command to be executed and can be used by just doing '?join' or '?j'.", color=discord.Color.dark_blue())

		embedLeave = discord.Embed(title = "?leave | ?l", description="This command will ask the bot to leave the current channel you are in. There are no additional arguements needed for this command to be executed and can be used by just doing '?leave' or '?l'.", color=discord.Color.dark_blue())

		embedPause = discord.Embed(title = "?pause", description="This command will pause the music that the bot is playing currently. There are no additional arguements needed for this command to be executed and can be used by just doing '?pause'.", color=discord.Color.dark_blue())

		embedResume = discord.Embed(title = "?resume | ?r", description="This command will resume the music that the bot was playing at the point it was paused at. There are no additional arguements needed for this command to be executed and can be used by just doing '?resume' or '?r'.", color=discord.Color.dark_blue())

		embedSkip = discord.Embed(title = "?skip | ?s", description="This command will skip to the next song in the queue. If there is no queue this command will just skip the current song and the bot will stop playing music. There are no additional arguements needed for this command to be executed and can be used by just doing '?skip' or '?s'.", color=discord.Color.dark_blue())

		embedStop = discord.Embed(title = "?stop", description="This command will stop the bot and kill all music being played, clear all current queues for the bot, and finally the bot will disconnect from the channel. This command is recommened if you are having troubles with the bot and wish to reset its current state. There are no additional arguements needed for this command to be executed and can be used by just doing '?stop'.", color=discord.Color.dark_blue())

		embedRestart = discord.Embed(title = "?restart", description="This command will restart the bot completely from the server end. This command should only be used incase of some emergency or persistent error that will not allow the bot to continue playing its music. There are no additional arguements needed for this command to be executed and can be used by just doing '?restart'.", color=discord.Color.dark_blue())

		embedVal = discord.Embed(title = "?valorant | ?val | ?v", description="This command will send back a randomly chosen valorant character to play. There are no additional arguements needed for this command to be executed and can be used by just doing '?valorant' or '?val' or '?v'.", color=discord.Color.dark_blue())

		embedOw = discord.Embed(title = "?overwatch | ?ow | ?o", description="This command will send back a randomly chosen overwatch character to play. There are no additional arguements needed for this command to be executed and can be used by just doing '?overwatch' or '?ow' or '?o'.", color=discord.Color.dark_blue())

		embedValOv = discord.Embed(title = "?ov", description="This command will send back a randomly chosen valorant and overwatch character to play. There are no additional arguements needed for this command to be executed and can be used by just doing '?ov'.", color=discord.Color.dark_blue())
except Exception as error:
		print(f"There was an error embeding the help command: {error}")

class Help(commands.HelpCommand):

		def __init__(self):
				super().__init__()

		async def send_bot_help(self, mapping):
				await self.get_destination().send(embed = embedHelp)

		async def send_command_help(self, command):
				command = str(command).strip()	

				if command == 'play' or  command == 'p':
						await self.get_destination().send(embed = embedPlay)
				elif command == 'queue' or  command == 'que' or command == 'q':
						await self.get_destination().send(embed = embedQueue)
				elif command == 'qlist' or command == 'ql':
						await self.get_destination().send(embed = embedQueueList)
				elif command == 'clearq' or  command == 'q':
						await self.get_destination().send(embed = embedClearQ)
				elif command == 'removeq' or  command == 'rq':
						await self.get_destination().send(embed = embedRemoveQ)
				elif command == 'loop' or 'loop1':
						await self.get_destination().send(embed = embedLoop)
				elif command == 'join' or  command == 'j':
						await self.get_destination().send(embed = embedJoin)
				elif command == 'leave' or  command == 'l':
						await self.get_destination().send(embed = embedLeave)
				elif command == 'pause':
						await self.get_destination().send(embed = embedPause)
				elif command == 'resume' or  command == 'r':
						await self.get_destination().send(embed = embedResume)
				elif command == 'skip' or  command == 's':
						await self.get_destination().send(embed = embedSkip)
				elif command == 'stop':
						await self.get_destination().send(embed = embedStop)
				elif command == 'restart':
						await self.get_destination().send(embed = embedRestart)
				elif command == 'valorant' or  command == 'val' or command == 'v':
						await self.get_destination().send(embed = embedVal)
				elif command == 'overwatch' or  command == 'ow' or command == 'o':
						await self.get_destination().send(embed = embedOw)
				elif command == 'ov':
						await self.get_destination().send(embed = embedValOv)
				else:
						await self.get_destination().send(f"```The command {command} was not found in the list of help [commands]. Please check your spelling of the command or that it is actually a valid command.```")
						return

				return
				
# Creating the bot to interact with events/commands in discord. 
bot = commands.Bot(command_prefix = '?', help_command = Help())

# Link to invite bot with proper permissions:

for file in os.listdir('./cogs'):
		if file.endswith('.py'):
				bot.load_extension(f"cogs.{file[:-3]}")

# Starts the bot client.
bot.run(config('token'))
