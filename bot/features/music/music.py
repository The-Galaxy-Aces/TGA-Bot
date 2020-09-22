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

        # TODO: In addition to the currSong, maybe grab additional metadata from the file for display
        self.currSong = ""

    def playNext(self):
        if len(self.queue) > 0:
            self.currSong = self.queue.pop()
            self.voiceClient.play(discord.FFmpegPCMAudio(self.currSong),
                                  after=lambda e: self.playNext())
            self.voiceClient.is_playing()

    # TODO: If using a local library for music, load all the local music into
    # A database so that we can quickly search and find music to play
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music is ready!")

    @commands.command()
    async def music(self, ctx, *args):

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
                            # TODO: Only allow certain media types (exclude
                            # things like jpg which may be cover art included
                            # with the album)
                            # print(root2 + "/" + file)
                            self.queue.append(root2 + "/" + file)

        random.shuffle(self.queue)

        if type(self.voiceClient) is str or not self.voiceClient.is_connected(
        ):
            channel = ctx.guild.get_channel(
                ctx.message.author.voice.channel.id)
            self.voiceClient = await channel.connect()

        self.currSong = self.queue.pop()
        self.voiceClient.play(discord.FFmpegPCMAudio(self.currSong),
                              after=lambda e: self.playNext())
        self.voiceClient.is_playing()

    @commands.command()
    async def next(self, ctx):
        self.voiceClient.stop()
        self.playNext()

    @commands.command()
    async def stop(self, ctx):
        self.queue = []
        self.voiceClient.stop()

    @commands.command()
    async def currentSong(self, ctx):
        await ctx.message.channel.send(self.currSong)
