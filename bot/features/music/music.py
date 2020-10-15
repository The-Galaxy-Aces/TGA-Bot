import discord
import os
import fnmatch
import random
import audio_metadata
import threading
from time import sleep
import pathlib
from discord.ext import commands
from bot.features.tgacog import TGACog


class Music(TGACog):
    """
    Sit back and enjoy some chill tunes
    """
    def __init__(self, bot):
        # Required for the bot:
        self.bot = bot
        self._last_member = None
        self.ready = False

        # Used for music playback and functions
        self.currQueue = []
        self.voiceClient = ""
        self.currSong = 0
        self.currVolume = 1.0
        self.didPrevExecute = False
        self.searchPattern = ""
        self.localLibrary = {}
        self.initalLock = True

        REQUIRED_PARAMS = ['local_path', 'audio_types', 'search_frequency']
        self.processConfig(self.bot, REQUIRED_PARAMS)

        self.localPath = self.CONFIG['local_path']
        self.audioTypes = self.CONFIG['audio_types']
        self.searchFrequency = self.CONFIG['search_frequency']  # In seconds

        # Only create the thread to search the local library if it is enabled
        if self.localPath:
            self.searchThread = threading.Thread(target=self.searchingThread,
                                                 daemon=True)
            self.searchThread.start()

    def searchingThread(self):
        '''
        searchingThread is spawned as a seperate daemon thread from the main process
        It executes its search every self.searchFrequency seconds in order to update
        the music library as it is changed.
        # TODO this can probably be refactored with discord.py tasks:
        https://discordpy.readthedocs.io/en/latest/ext/tasks/index.html
        '''
        while (True):
            self.bot.log.debug("searchingThread Executing")

            self.localLibrary = []
            rootdir = self.localPath
            rootdir = rootdir.rstrip(os.sep)
            for path, _, files in os.walk(rootdir):
                filterdFiles = [
                    f"{path}/{file}" for file in files
                    if pathlib.Path(file).suffix in self.audioTypes
                ]
                self.localLibrary += filterdFiles

            self.bot.log.debug(
                f"searchingThread Completed. Loaded {len(self.localLibrary)} songs."
            )

            # initalLock is used to lock the music function until the first search after
            # starting the bot is completed. Otherwise searches would fail or return partial
            # results until the initial search is completed.
            # TODO maybe we can put something into a pre invoke method to populate the local
            # library before the bot accepts music commands
            if self.initalLock:
                self.initalLock = False

            sleep(self.searchFrequency)

    def searchLibrary(self, pattern):

        return [
            song for song in self.localLibrary
            if fnmatch.fnmatch(f"{song}", f"*{pattern}*")
        ]

    def playNext(self):
        if self.currSong >= 0 and self.currSong < len(self.currQueue):
            self.voiceClient.play(discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(self.currQueue[self.currSong],
                                       options="-loglevel panic"),
                self.currVolume),
                                  after=lambda e: self.finishedSong())
        else:
            self.voiceClient.stop()

    def finishedSong(self):
        self.currSong += 1
        self.playNext()

    @commands.group(aliases=['m'])
    async def music(self, ctx, *args):
        '''
        Searches for an artist, album, or song and places
        all the matches into the queue and starts playing.
        '''

        # Wait for the inital search to complete before trying to play music. This only occurs
        # once immediately after the bot is started.
        while self.initalLock:
            self.bot.log.debug("Waiting for initalLock to unlock")
            sleep(1)

        newQueue = []

        if ctx.message.author.voice is None:

            await ctx.message.channel.send(
                "```You need to join a voice channel in order to listen to music.```"
            )
            return

        try:
            await ctx.bot.fetch_channel(ctx.message.author.voice.channel.id)
        except Exception:
            await ctx.message.channel.send(
                f"```I do not have permissions to join the channel: {ctx.message.author.voice.channel}.```"
            )
            return

        if len(args) == 0:
            await ctx.send('\n'.join((
                "```To play music, search for an artist, album, or song using:",
                f"{self.bot.command_prefix}music search criteria",
                f"Example: {self.bot.command_prefix}music Sgt. Pepper's Lonely Hearts Club Band```"
            )))
            return

        newQueue = self.searchLibrary(' '.join(args))

        if len(newQueue) == 0:
            await ctx.message.channel.send(
                f"```Sorry, I couldn't find any music which matches your search critera: {' '.join(args)}```"
            )
            return

        self.currQueue.clear()
        self.currSong = 0

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
                "```You need to join a voice channel in order to listen to music.```"
            )
            return

        self.currQueue = newQueue

        random.shuffle(self.currQueue)

        self.playNext()
        await ctx.message.channel.send(
            f"```Now playing: {self.getSongMetadata(self.currQueue[self.currSong])}```"
        )

    @music.command(aliases=['q'])
    async def queue(self, ctx):
        '''
        Displays information about the current song queue.
        '''
        if self.currQueue:
            queueString = [
                f"{f'Previous song: {self.getSongMetadata(self.currQueue[self.currSong-1])}' if self.currSong > 0 else ''}"
            ]

            queueString.append(
                f"{f'Current song: {self.getSongMetadata(self.currQueue[self.currSong])}' if self.currSong >= 0 else ''}"
            )
            queueString.append(
                f"{f'Next song: {self.getSongMetadata(self.currQueue[self.currSong+1])}' if self.currSong + 1 < len(self.currQueue) else ''}"
            )
            sep = "\n"
            await ctx.message.channel.send(f'''
                ```{sep.join(queueString)}```
                ''')
        else:
            await ctx.message.channel.send('''
                ```The music queue is currently empty.```
                ''')

    @music.command(aliases=['n'])
    async def next(self, ctx):
        '''
        Plays the next song in the queue.
        '''
        self.voiceClient.stop()

    @next.after_invoke
    async def after_next(self, ctx):
        if self.currSong + 1 < len(self.currQueue):
            await ctx.message.channel.send(
                f"```Now playing: {self.getSongMetadata(self.currQueue[self.currSong + 1])}```"
            )
        else:
            await self.voiceClient.disconnect()
            await ctx.message.channel.send(
                f"```Playback complete. Use the {self.bot.command_prefix}music command to search for and playback more music.```"
            )

    @music.command(aliases=['p'])
    async def prev(self, ctx):
        '''
        Plays the previous song in the queue.
        '''
        if self.currSong > 0:
            self.currSong -= 2
            self.voiceClient.stop()
            self.didPrevExecute = True
        else:
            await ctx.message.channel.send(
                "```You're already at the beginning of the queue.```")

    @prev.after_invoke
    async def after_prev(self, ctx):
        if self.didPrevExecute:
            self.didPrevExecute = False
            await ctx.message.channel.send(
                f"```Now playing: {self.getSongMetadata(self.currQueue[self.currSong + 1])}```"
            )

    @music.command(aliases=['s'])
    async def stop(self, ctx):
        '''
        Stop the audio stream and clear the music queue.
        '''
        self.currQueue.clear()
        self.currSong = 0
        self.voiceClient.stop()
        await self.voiceClient.disconnect()

    @music.command(aliases=['pa'])
    async def pause(self, ctx):
        '''
        Pauses the current song.
        '''
        if self.voiceClient.is_playing():
            self.voiceClient.pause()

    @music.command(aliases=['r'])
    async def resume(self, ctx):
        '''
        Resumes the current song.
        '''
        if self.voiceClient.is_paused():
            self.voiceClient.resume()

    @music.command(aliases=['cs'])
    async def currentSong(self, ctx):
        '''
        Displays metadata for the current song.
        '''
        if self.currSong >= 0 and self.currSong < len(self.currQueue):
            await ctx.message.channel.send(
                f"```Now playing: {self.getSongMetadata(self.currQueue[self.currSong])}```"
            )

    @music.command(aliases=['v'])
    async def volume(self, ctx, args):
        '''
        Adjusts the volume to the specified level.
        Where <args> is an integer between 0 and 100
        '''
        try:
            myVolume = int(args)
            if myVolume >= 0 and myVolume <= 100:
                self.voiceClient.source.volume = self.currVolume = myVolume / 100
            else:
                raise Exception("Invalid Value")
        except Exception:
            await ctx.message.channel.send(
                "For volume please enter a value between 0 and 100.")

    @music.command(aliases=['c'])
    async def come(self, ctx):
        '''
        Moves the bot to the your current voice channel.
        '''
        if ctx.message.author.voice is None:

            await ctx.message.channel.send(
                "```You need to join a voice channel in order to listen to music.```"
            )
            return

        try:
            await ctx.bot.fetch_channel(ctx.message.author.voice.channel.id)
        except Exception:
            await ctx.message.channel.send(
                f"```I do not have access to join the channel: {ctx.message.author.voice.channel}.```"
            )
            return

        if not isinstance(self.voiceClient,
                          str) and self.voiceClient.is_playing():
            channel = ctx.guild.get_channel(
                ctx.message.author.voice.channel.id)
            await self.voiceClient.move_to(channel)
        else:
            await ctx.message.channel.send(
                "```I need to be playing music in order to come to your channel.```"
            )

    def getSongMetadata(self, song):
        try:
            md = audio_metadata.load(song)
            artist = md["tags"]["albumartist"]
            if not artist:
                artist = md["tags"]["artist"]
            title = md["tags"]["title"]
            album = md["tags"]["album"]
        except Exception as e:
            self.bot.log.error(f"{song} has invalid metadata: {e}")
            return (f"{song.split(os.sep)[-1]} has invalid metadata.")

        return f"{title[0]} by: {artist[0]} from: {album[0]}."
