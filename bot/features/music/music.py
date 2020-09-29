import requests
import html
import discord
import os
import fnmatch
import random
import audio_metadata
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
        self.currSong = 0
        self.currVolume = 1.0

    def playNext(self):
        if len(self.queue) > 0 and self.currSong < len(self.queue):
            self.voiceClient.play(discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(self.queue[self.currSong]),
                self.currVolume),
                                  after=lambda e: self.finishedSong())
            self.voiceClient.is_playing()
        else:
            self.voiceClient.stop()

    def adjustQueue(self):
        self.currSong -= 2

    # TODO: If using a local library for music, load all the local music into
    # A database so that we can quickly search and find music to play

    def finishedSong(self):
        self.currSong += 1
        self.playNext()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music is ready!")

    @commands.command()
    async def music(self, ctx, *args):

        newQueue = []

        if len(args) == 0:
            await ctx.send('\n'.join((
                "To play music, search for an artist, album, or song using:",
                f"{self.bot.command_prefix}music search criteria",
                f"Example: {self.bot.command_prefix}music Sgt. Pepper's Lonely Hearts Club Band"
            )))
            return

        # TODO: Major cleanup of the searching
        for root, dirs, files in os.walk(self.localPath):
            for dir in dirs:
                if fnmatch.fnmatch(dir, "*" + ' '.join(args) + "*"):
                    for root2, dirs2, files2 in os.walk(root + "/" + dir):
                        for file in files2:
                            if file.endswith('.mp3') or file.endswith(
                                    '.mp4'
                            ) or file.endswith('.flac') or file.endswith(
                                    '.ogg') or file.endswith(
                                        '.m4a') or file.endswith(
                                            '.wav') or file.endswith('.wma'):
                                newQueue.append(root2 + "/" + file)

        if len(newQueue) == 0:
            await ctx.message.channel.send(
                f"Sorry, I couldn't find any music which matches your search critera: {' '.join(args)}"
            )
            return

        self.queue = newQueue

        random.shuffle(self.queue)

        if type(self.voiceClient) is str or not self.voiceClient.is_connected(
        ):
            channel = ctx.guild.get_channel(
                ctx.message.author.voice.channel.id)
            self.voiceClient = await channel.connect()
        else:
            self.voiceClient.stop()

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

    @commands.command()
    async def currentSong(self, ctx):
        if len(self.queue) > 0 and self.currSong < len(self.queue):
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
