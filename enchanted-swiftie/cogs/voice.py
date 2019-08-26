import os
import random

import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from googleapiclient.discovery import build


class VoiceModule(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.country_songs = []
        self.pop_songs = []
        self.read_songs()
        with open(r"resources\google-token.txt", "rt") as youtube_token_file:
            self.youtube_client = build("youtube", "v3", developerKey=youtube_token_file.readline().rstrip())

    @commands.command(aliases=["play", "p"])
    async def command_play(self, ctx: commands.Context, *, song: str = ""):
        """Plays a choosen/random taylor song"""
        try:
            await self.join(ctx)
        except AttributeError:
            # Already handled the exception inside the join function, just need to exit the play function
            return
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        # Can't play another file while we're currently playing
        if voice_client.is_playing():
            await ctx.send("Please wait until the song ends")
            return
        # Getting ready to download a new file
        elif os.path.isfile(".\\file.mp3"):
            os.remove(".\\file.mp3")
        # User isn't in any voice channel, the join command already sent an error message,
        # just need to exit out of the function
        if voice_client is None:
            return
        # Choose a the name of a random taylor song
        if song.strip() == "":
            song = random.choice(self.country_songs + self.pop_songs)
        elif song.strip() == "pop":
            song = random.choice(self.pop_songs)
        elif song.strip() == "country":
            song = random.choice(self.country_songs)
        song = "Taylor Swift " + song
        # Creating an Http Request for the video
        url_request = self.youtube_client.search().list(q=song, part="snippet", type="video")
        # Executing it
        url_request = url_request.execute()
        # prob a smarter way to do it, getting the video suffix from the HttpRequest
        video_suffix = list(url_request.values())[5][0]['id']['videoId']
        video_url = "https://www.youtube.com/watch?v=" + video_suffix
        # Just sort of default options
        ydl_opts = {
            "format": "bestaudio/audio",
            "postprocessors":
            [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
        # Downloading the file
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Renaming the file to "file"
        for file in os.listdir(".\\"):
            if file.endswith(".mp3"):
                os.rename(file, "file.mp3")

        # Playing the file
        await ctx.send(f"Now playing: {video_url}")
        voice_client.play(discord.FFmpegPCMAudio("file.mp3"))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = 0.2

    @commands.command(aliases=["end", "e"])
    async def command_end(self, ctx: commands.Context):
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        # The bot isn't connected to the server
        if voice_client is None:
            await ctx.send("Bot isn't in any voice channel")
        # The bot is connected and playing music
        elif voice_client.is_playing():
            await ctx.send("Song successfully stopped")
            await voice_client.stop()
        # The bot is connected but isn't playing any music
        else:
            await ctx.send("Bot isn't playing any music")

    @commands.command(aliases=["disconnect", "d"])
    async def command_disconnect(self, ctx: commands.Context):
        """"Disconnects the bot from a voice channel"""
        # goes the voice client belonging to the author's server
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        # checks if the voice channel of the sender is the same channel the bot is currently at
        if vc.channel == ctx.author.voice.channel:
            await vc.disconnect()
        else:
            await ctx.send("Can't disconnect the bot from outside the voice channel")

    async def join(self, ctx: commands.Context):
        """Establishes connection with a voice channel"""
        try:
            voice_channel = ctx.author.voice.channel
        except AttributeError:
            await ctx.send("User isn't in any voice channel")
            return AttributeError

        # get the voice client of the server
        voice_client = get(self.bot.voice_clients, guild=ctx.guild)
        # if the bot isn't already connected to the server voice client, we establish a connection
        if voice_client is None:
            # Need to connect - then disconnect - then connect again, otherwise it won't play sound
            await voice_channel.connect()
            voice_client = get(self.bot.voice_clients, guild=ctx.guild)
            await voice_client.disconnect()
            await voice_channel.connect()
        # if the bot is already connected to the server voice client, we only move him to the right channel
        else:
            await voice_client.move_to(voice_channel)

    def read_songs(self):
        """Reads the tay-songs file and populates the country_songs and pop_songs lists"""
        is_pop = False
        with open(r"resources\tay-songs.txt", "r") as tay_songs:
            for line in tay_songs:
                line = line.rstrip("\n")
                if not is_pop:
                    if line == "pop":
                        is_pop = True
                        continue
                    self.country_songs.append(line)
                else:
                    self.pop_songs.append(line)

