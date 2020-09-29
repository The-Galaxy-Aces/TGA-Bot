import discord
import os
import fnmatch
import random
import audio_metadata
import threading
from time import sleep
import pathlib
from discord.ext import commands


class Music(commands.Cog):
    """The Music class
    Sit back and enjoy some chill tunes
    """
    def __init__(self, bot):

        self.bot = bot
        self._last_member = None
        self.queue = []
        self.voiceClient = ""
        self.localPath = bot.enabled_features['music']['localPath']
        self.audioTypes = [".flac", ".mp3", ".mp4", ".ogg", ".wav", ".wma"]
        self.currSong = 0
        self.currVolume = 1.0

        self.searchPattern = ""

        self.localLibrary = {}

        self.processConfig()

        self.searchThread = threading.Thread(target=self.searchingThread,
                                             daemon=True)

        self.searchThread.start()

    def searchingThread(self):
        while (True):

            self.localLibrary = []
            rootdir = self.localPath
            rootdir = rootdir.rstrip(os.sep)
            start = rootdir.rfind(os.sep) + 1
            for path, dirs, files in os.walk(rootdir):
                folders = path[start:].split(os.sep)
                filterdFiles = [
                    f"{path}/{file}" for file in files
                    if pathlib.Path(file).suffix in self.audioTypes
                ]
                self.localLibrary += filterdFiles

            sleep(20)

    def searchLibrary(self, pattern):

        newQueue = []

        for song in self.localLibrary:
            if fnmatch.fnmatch(f"{song}", f"*{pattern}*"):
                newQueue.append(song)
        return newQueue

    def playNext(self):
        if self.currSong >= 0 and self.currSong < len(self.queue):
            self.voiceClient.play(discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(self.queue[self.currSong]),
                self.currVolume),
                                  after=lambda e: self.finishedSong())
            self.voiceClient.is_playing()
        else:
            self.voiceClient.stop()

    def processConfig(self):
        '''
        # TODO: Process the config (once merged with the threaded bots branch)
        '''

    def adjustQueue(self):
        self.currSong -= 2

    def finishedSong(self):
        self.currSong += 1
        self.playNext()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music is ready!")

    @commands.command()
    async def music(self, ctx, *args):

        newQueue = []

        if ctx.message.author.voice is None:

            await ctx.message.channel.send(
                f"{ctx.message.author.mention} you need to join a voice channel in order to listen to music."
            )
            return

        if len(args) == 0:
            await ctx.send('\n'.join((
                "To play music, search for an artist, album, or song using:",
                f"{self.bot.command_prefix}music search criteria",
                f"Example: {self.bot.command_prefix}music Sgt. Pepper's Lonely Hearts Club Band"
            )))
            return

        newQueue = self.searchLibrary(' '.join(args))

        if len(newQueue) == 0:
            await ctx.message.channel.send(
                f"Sorry, I couldn't find any music which matches your search critera: {' '.join(args)}"
            )
            return

        self.queue = newQueue

        random.shuffle(self.queue)

        try:
            if isinstance(self.voiceClient,
                          str) or not self.voiceClient.is_connected():
                channel = ctx.guild.get_channel(
                    ctx.message.author.voice.channel.id)
                self.voiceClient = await channel.connect()
            else:
                self.voiceClient.stop()
        except AttributeError:
            await ctx.message.channel.send(
                "You need to join a voice channel in order to listen to music."
            )
            return

        self.playNext()
        await ctx.message.channel.send(
            f"Now playing: {getSongMetadata(self.queue[self.currSong])}")

    @commands.command()
    async def next(self, ctx):
        self.voiceClient.stop()

    @next.after_invoke
    async def after_next(self, ctx):
        await ctx.message.channel.send(
            f"Now playing: {getSongMetadata(self.queue[self.currSong + 1])}")

    @commands.command()
    async def prev(self, ctx):
        self.adjustQueue()
        self.voiceClient.stop()

    @prev.after_invoke
    async def after_prev(self, ctx):
        await ctx.message.channel.send(
            f"Now playing: {getSongMetadata(self.queue[self.currSong + 1])}")

    @commands.command()
    async def stop(self, ctx):
        self.queue.clear()
        self.currSong = 0
        self.voiceClient.stop()
        await self.voiceClient.disconnect()

    @commands.command()
    async def pause(self, ctx):
        '''TODO: Pause the audio stream and then resume it later.'''

    @commands.command()
    async def currentSong(self, ctx):
        if self.currSong >= 0 and self.currSong < len(self.queue):
            await ctx.message.channel.send(
                f"Now playing: {getSongMetadata(self.queue[self.currSong])}")

    @commands.command()
    async def volume(self, ctx, args):
        try:
            myVolume = int(args)
            if myVolume >= 0 and myVolume <= 100:
                self.voiceClient.source.volume = self.currVolume = myVolume / 100
            else:
                raise Exception("Invalid Value")
        except Exception:
            await ctx.message.channel.send(
                f"For volume please enter a value between 0 and 100.")


def getSongMetadata(song):
    try:
        md = audio_metadata.load(song)
        artist = md["tags"]["albumartist"]
        if not artist:
            artist = md["tags"]["artist"]
        title = md["tags"]["title"]
        album = md["tags"]["album"]
    except Exception as e:
        print(f"ERROR: on song {song}: {e}")
        return (f"Sorry, {song} has some invalid metadata.")

    return f"{title[0]} by: {artist[0]} from: {album[0]}."
