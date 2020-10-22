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
        self.process_config(self.bot, REQUIRED_PARAMS)

        self.uri = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        self.my_insult = ""

        self.torment_list = []

        self.permissions = self.get_permissions(self.bot)

    def generate_insult(self):
        resp = requests.get(self.uri)
        if resp.status_code == 200:
            self.my_insult = resp.json()["insult"]
        else:
            raise Exception(
                "Insult.generate_insult: Error in request: Status Code!=200")

    def get_insult(self):
        self.generate_insult()
        return html.unescape(self.my_insult)

    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        Activates on every message which is sent which the bot has access to read.
        '''
        # Torment a user if they exist in the torment list and sent the message.
        for tormented in self.torment_list:
            if tormented == message.author.mention:
                await message.channel.send(f"{tormented} {self.get_insult()}")

    @commands.group(aliases=['i'])
    @TGACog.check_permissions()
    async def insult(self, ctx):
        '''
        Generates an insult against the mentioned user(s)
        '''
        if ctx.message.author == self.bot.user:
            return
        else:
            if ctx.invoked_subcommand is None:
                for mention in ctx.message.mentions:
                    await ctx.message.channel.send(
                        f"{mention.mention} {self.get_insult()}")

    @insult.command(aliases=['t'])
    @TGACog.check_permissions()
    async def torment(self, ctx):
        '''
        Torments the mentioned user(s) by insulting them with every message.
        '''
        for mention in ctx.message.mentions:
            if mention.mention not in self.torment_list \
                    and mention.mention != ctx.bot.user.mention:
                self.torment_list.append(mention.mention)

    @insult.command(aliases=['u'])
    @TGACog.check_permissions()
    async def untorment(self, ctx):
        '''
        Removes the endless torment from the mentioned user(s).
        '''
        for mention in ctx.message.mentions:
            self.torment_list.remove(mention.mention)

    @insult.error
    @torment.error
    @untorment.error
    async def insult_cmd_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send(f"Error in Insult: {error}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.channel.send(
                "You do not have permissions to use that command.")
