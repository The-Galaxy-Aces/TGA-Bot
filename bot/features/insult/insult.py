import requests
import html
from discord.ext import commands
from bot.features.tgacog import TGACog


class Insult(TGACog):
    '''
    Auto generate some insults and hurt your friends.
    '''
    def __init__(self, bot):
        """
        Don't let the mean insults hurt your feelings
        """
        self.bot = bot
        self._last_member = None
        self.ready = False

        # TODO: allow for a variety of insults from different APIs
        # TODO: ADD: https://insult.mattbas.org/api
        # TODO: ADD: https://generatorfun.com/insult-generator

        REQUIRED_PARAMS = []
        self.processConfig(self.bot, REQUIRED_PARAMS)

        self.uri = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        self.myInsult = ""

        self.tormentList = []

    def generateInsult(self):
        resp = requests.get(self.uri)
        if resp.status_code == 200:
            self.myInsult = resp.json()["insult"]
        else:
            raise Exception(
                "Insult.generate_insult: Error in request: Status Code!=200")

    def getInsult(self):
        self.generateInsult()
        return html.unescape(self.myInsult)

    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Activates on every message which is sent which the bot has access to read.
        '''
        # Torment a user if they exist in the torment list and sent the message.
        for tormented in self.tormentList:
            if tormented == message.author.mention:
                await message.channel.send(f"{tormented} {self.getInsult()}")

    @commands.group(aliases=['i'])
    async def insult(self, ctx):
        '''
        Generates an insult against the mentioned user(s)
        '''
        if ctx.message.author == self.bot.user:
            return
        else:
            for mention in ctx.message.mentions:
                await ctx.message.channel.send(
                    f"{mention.mention} {self.getInsult()}")

    @insult.command(aliases=['t'])
    async def torment(self, ctx):
        '''
        Torments the mentioned user(s) by insulting them with every message.
        '''
        for mention in ctx.message.mentions:
            if mention.mention not in self.tormentList \
                    and mention.mention != ctx.bot.user.mention:
                self.tormentList.append(mention.mention)

    @insult.command(aliases=['u'])
    async def untorment(self, ctx):
        '''
        Removes the endless torment from the mentioned user(s).
        '''
        for mention in ctx.message.mentions:
            self.tormentList.remove(mention.mention)

    @insult.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send(f"Error in Insult: {error}")
