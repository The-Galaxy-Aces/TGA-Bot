from discord.ext import commands
from bot.features.tgacog import TGACog


class Poll(TGACog):
    def __init__(self, bot):

        self.bot = bot

        self.polls = {}
        self.cmd = ""

    @commands.command()
    async def poll(self, ctx, *args):
        '''
        Create a new poll.
        Usage:
        '''
        print(args)
        cmd = args

        if cmd[0] == "create":
            self.create(cmd[1:])
            await ctx.message.channel.send(
                f"""````A new poll is available: {self.polls}```""")
        elif cmd[0] == "stats":
            self.stats(cmd[1:])
        elif cmd[0] == "vote":
            self.vote(cmd[1:])
        else:
            help(self)

        await ctx.message.delete()

    @commands.command()
    async def list(self, ctx, *args):
        print("list")

    def create(self, cmd):
        '''
        Creates a new poll
        useage: poll create YOUR POLL NAME : VALUE1 : VALUE2 : VALUE3 : ... : VALUEN
        '''

        params = ' '.join(cmd).split(' : ')
        print(f"params: {params}")

        if len(params) < 3:
            print("Not enough values")
            return

        pollName = params[0]
        pollValues = dict.fromkeys(params[1:], 0)
        print(f"pollName: {pollName}")

        if not self.polls.get(pollName):
            self.polls.update({pollName: pollValues})
        else:
            # TODO if the poll exists then show a message
            pass

        print(self.polls)

    def vote(self, cmd):
        # TODO Check if the user has already voted and reject if they do
        self.polls[cmd[0]][cmd[1]] += 1

    def stats(self, cmd):
        pass
