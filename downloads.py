# All the imported packages needed to run this cog.
import discord
from discord.ext import commands

import os
import shutil
from decouple import config

from pytube import YouTube, Search
from spotdl.search import SpotifyClient
from spotdl.parsers import parse_query

# Initialize spotify client
SpotifyClient.init(
    client_id=config('SClientID'),
    client_secret=config('SClientSecret'),
    user_auth=False
)

def downloadSong(songInfo, serverID):
		print("Trying to download song")
		download_path = f"./servers/main{serverID}"
		
		# Downloading the youtube audio
		if ('https' in songInfo) and ('youtube' in songInfo):
				vid = YouTube(songInfo)
				fout = vid.streams.get_audio_only().download(download_path)

		elif ('https' in songInfo) or ('spotify' in songInfo):
				song_list = parse_query(
						[songInfo],
						"mp3",
						False,
						False,
						None,
						1,
						None
				)

				youtube_link = song_list[0].youtube_link

				vid = YouTube(youtube_link)
				fout = vid.streams.get_audio_only().download(download_path)
			
		else:
				song_list = parse_query(
						[songInfo],
						"mp3",
						False,
						False,
						None,
						1,
						None
				)

				if song_list:
						youtube_link = song_list[0].youtube_link
						vid = YouTube(youtube_link)
						fout = vid.streams.get_audio_only().download(download_path)

				else:
						# Search for the song through youtube instead
						search = Search(songInfo)
						vid = search.results[0]
						fout = search.results[0].streams.get_audio_only().download(download_path)					
						
		os.rename(fout, f"/home/ubuntu/Bot-Bot/servers/main{serverID}/song.mp3")
					
		return vid


def downloadSongQ(songInfo, q_num, serverID):
		download_path = f"/home/ubuntu/Bot-Bot/servers/main{serverID}/SetupSong"
		queue_dir = f"/home/ubuntu/Bot-Bot/servers/main{serverID}/Queue"

		# Downloading the youtube audio
		if ('https' in songInfo) and ('youtube' in songInfo):
				vid = YouTube(songInfo)
				fout = vid.streams.get_audio_only().download(download_path)
				
		elif ('https' in songInfo) and ('spotify' in songInfo):
				song_list = parse_query(
						[songInfo],
						"mp3",
						False,
						False,
						None,
						1,
						None
				)

				youtube_link = song_list[0].youtube_link
				vid = YouTube(youtube_link)
				fout = vid.streams.get_audio_only().download(download_path)
			
		else:
				song_list = parse_query(
						[songInfo],
						"mp3",
						False,
						False,
						None,
						1,
						None
				)
			
				if song_list:
						youtube_link = song_list[0].youtube_link
						vid = YouTube(youtube_link)
						fout = vid.streams.get_audio_only().download(download_path)

				else:
						# Search for the song through youtube instead
						search = Search(songInfo)
						vid = search.results[0]
						fout = vid.streams.get_audio_only().download(download_path)

		os.rename(fout, f"/home/ubuntu/Bot-Bot/servers/main{serverID}/SetupSong/song{q_num}.mp3")
		shutil.move(f"/home/ubuntu/Bot-Bot/servers/main{serverID}/SetupSong/song{q_num}.mp3", queue_dir)
	
		return vid

def getSongData(data, context, q_num=None, queue=False):

		# Getting the information that is going to be used more than once to create the embeded or needs to be calculated for a time.
		webpage_url = data.watch_url
		duration = get_duration(int(data.length))
		thumbnail = data.thumbnail_url
		release = data.publish_date
		artist = data.author

		if queue:
				embed = (discord.Embed(title='Queuing Song:',
						description=f"```\n{data.title} {artist}\n```",
						color=discord.Color.dark_blue())
						.set_author(name="Song Requester: " + context.author.display_name, icon_url= context.author.avatar_url)
						.add_field(name='Duration', value=duration)
						.add_field(name='Release Date', value=release)
						.add_field(name='Channel', value=f"[{data.author}]({data.channel_url})")
						.add_field(name='URL', value=f"[{data.title} - {artist}]({webpage_url})")
						.add_field(name='Queue Position', value=q_num)
						.set_thumbnail(url=thumbnail)
						)
		else:
				embed = (discord.Embed(title="Now playing: ", description = f"```css\n{data.title} {artist}\n```",
						color=discord.Color.dark_blue())
						.set_author(name="Song Requester: " + context.author.display_name, icon_url= context.author.avatar_url)
						.add_field(name='Duration', value=duration)
						.add_field(name='Release Date', value=release)
						.add_field(name='Channel', value=f"[{data.author}]({data.channel_url})")
						.add_field(name='URL', value=f"[{data.title} - {data.author}]({webpage_url})")
						.set_thumbnail(url=thumbnail)
						)

		return embed


def get_duration(duration: int):
		minutes, seconds = divmod(duration, 60)
		hours, minutes = divmod(minutes, 60)
		days, hours = divmod(hours, 24)

		duration = []
		if days > 0:
				duration.append(f'{days}')
		if hours > 0:
			if hours < 9:
				hours = str(0) + str(hours)
			duration.append(f'{str(hours)}')
		if minutes > 0:
			if minutes < 9:
				minutes = str(0) + str(minutes)
			duration.append(f'{str(minutes)}')
		if seconds > 0:
			if seconds < 9:
				seconds = str(0) + str(seconds)
			duration.append(f'{str(seconds)}')
		
		timeSong = ""
		for i in duration:
				if duration.index(i) == len(duration) - 1:
						timeSong += (i)
				else:
						timeSong += (i + ":")

		return timeSong