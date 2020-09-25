import requests
import html
import discord
import os
import fnmatch
import random
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
        self.localPath = "/music"
        self.currSong = 0

    def playNext(self):

        if len(self.queue) > 0 and self.currSong < len(self.queue):
            self.voiceClient.play(discord.FFmpegPCMAudio(
                self.queue[self.currSong]),
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
            await ctx.send(
                "To play music, search for an album using:\n!music ALBUM_NAME")
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
                "Sorry, I couldn't find any music which matches your search critera: "
                + ' '.join(args))
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
        await ctx.message.channel.send("Now playing: " +
                                       self.queue[self.currSong])

    @commands.command()
    async def next(self, ctx):
        self.voiceClient.stop()
        await ctx.message.channel.send("Now playing: " +
                                       self.queue[self.currSong + 1])

    @commands.command()
    async def prev(self, ctx):
        self.adjustQueue()
        self.voiceClient.stop()
        await ctx.message.channel.send("Now playing: " +
                                       self.queue[self.currSong + 1])

    @commands.command()
    async def stop(self, ctx):
        self.queue.clear()
        self.voiceClient.stop()

    @commands.command()
    async def currentSong(self, ctx):
        # TODO: In addition to the currSong, maybe grab additional metadata from the file for display
        await ctx.message.channel.send("Now playing: " +
                                       self.queue[self.currSong])
