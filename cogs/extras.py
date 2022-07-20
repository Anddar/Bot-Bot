# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

import random

def chooseValorant():
		# Agent List
		characters = ['Jett', 'Killjoy', 'Skye', 'Sova', 'Astra', 'Cypher', 'Kay/O', 'Omen', 'Pheonix', 'Raze', 'Reyna', 'Sage', 'Viper', 'Breach', 'Brimstone', 'Yoru']

		random.shuffle(characters) # Shuffle our list of characters

		# Returning the text saying what hero the user who called the command should play.	
		return f"```The Agent you should play in Valorant is: {characters[random.randint(0, len(characters))]}```"

def	chooseOverwatch():
		# Hero List
		characters = ['Ana', 'Ashe', 'Baptiste', 'Bastion', 'Brigette', 'D.Va', 'Doomfist', 'Echo', 'Genji', 'Hanzo', 'Junkrat', 'Lucio', 'McCree', 'Mei', 'Mercy', 'Moira', 'Orisa', 'Pharah', 'Reaper', 'Reinhardt', 'Roadhog', 'Sigma', 'Solder: 76', 'Sombra', 'Symmetra', 'Torbjorn', 'Tracer', 'Widowmaker', 'Winston', 'Wrecking Ball', 'Zarya', 'Zenyatta']

		random.shuffle(characters) # Shuffle our list of characters

		# Returning the text saying what hero the user who called the command should play.
		return f"```The Hero you should play as in Overwatch is: {characters[random.randint(0, len(characters))]}```"

class Extras(commands.Cog):

		def __init__(self, bot):
				self.bot = bot

		# Events


		# Commands

		@commands.command(help = "The command ?v will choose a random Agent to play as in Valorant.", pass_context = True, aliases = ['val', 'valorant'])
		async def v(self, ctx):
		    text = chooseValorant() # Calling function to choose a random Valorant character.
		    await ctx.channel.send(text) # Send the character they should play back to discord.
		    return

		@commands.command(help = "The command ?o will choose a random Hero to play as in Overwatch.", pass_context = True, aliases = ['ow', 'overwatch'])
		async def o(self, ctx):
		    text = chooseOverwatch() # Calling function to choose a random Overwatch character.
		    await ctx.channel.send(text) # Send the character they should play back to discord.
		    return

		@commands.command(help = "The command ?ov will choose a random Hero to play as in Overwatch and a random Agent to play in Valorant.", pass_context = True, aliases = [])
		async def ov(self, ctx):
		    text = chooseOverwatch() + '\n' + chooseValorant() # Calling function to choose a random Overwatch and Valorant character.
		    await ctx.channel.send(text) # Send the characters they should play back to discord.
		    return

def setup(bot):
		bot.add_cog(Extras(bot))