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
        self.insult = ""

    def generateInsult(self):
        resp = requests.get(self.uri)
        if resp.status_code == 200:
            self.insult = resp.json()["insult"]
        else:
            raise Exception(
                "Insult.generate_insult: Error in request: Status Code!=200")

    def getInsult(self):
        self.generateInsult()
        return html.unescape(self.insult)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Insults are ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        '''on_message left as an example for how to call it'''
        return

    @commands.command()
    async def insult(self, ctx):
        if ctx.message.author == self.bot.user:
            return
        else:
            for mention in ctx.message.mentions:
                await ctx.message.channel.send(mention.mention +
                                               self.getInsult())
