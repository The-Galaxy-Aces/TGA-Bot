import requests
import html
from discord.ext import commands


class Insult(commands.Cog):
    """The Insult class
    Don't let the mean insults hurt your feelings
    """
    def __init__(self, bot):
        """The Insult Cog
        Don't let the mean insults hurt your feelings
        """
        self.bot = bot
        self._last_member = None

        # TODO: allow for a variety of insults from different APIs
        # TODO: ADD: https://insult.mattbas.org/api
        # TODO: ADD: https://generatorfun.com/insult-generator

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
    async def on_ready(self):
        print("Insults are ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        for tormented in self.tormentList:
            if tormented == message.author.mention:
                await message.channel.send(f"{tormented} {self.getInsult()}")

    @commands.command()
    async def insult(self, ctx):
        if ctx.message.author == self.bot.user:
            return
        else:
            for mention in ctx.message.mentions:
                await ctx.message.channel.send(
                    f"{mention.mention} {self.getInsult()}")

    @commands.command()
    async def torment(self, ctx):
        for mention in ctx.message.mentions:
            if mention.mention not in self.tormentList:
                self.tormentList.append(mention.mention)

    @commands.command()
    async def untorment(self, ctx):
        for mention in ctx.message.mentions:
            self.tormentList.remove(mention.mention)
