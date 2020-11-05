from discord.ext import commands
from bot.features.tgacog import TGACog
import pprint


class Poll(TGACog):
    '''Create a Poll'''
    def __init__(self, bot):

        super().__init__(bot)

        self.polls = {}

    @commands.group(aliases=['p'])
    async def poll(self, ctx):
        '''Create a poll and spread democracy throughout your Discord!'''

    @poll.command(aliases=['l'])
    async def list(self, ctx, *args):
        '''
        Displays a list of all the polls

        If no params are entered, it will display a list of all polls.
        params:
            active [a] - Only display a list of active polls.
        '''

        active = False

        # TODO Clean this up
        if not args:
            active = False
        elif args[0].lower() in ["a", "active"]:
            active = True

        if not self.polls:
            return

        list_keys = []
        pre_text = f"Current list of {f'active ' if active else ''}polls"
        list_keys.append(pre_text)
        list_keys.append("```")
        for key in self.polls.keys():
            list_keys.append(key)

        list_keys.append("```")

        sep = "\n"
        await ctx.message.channel.send(f"{sep.join(list_keys)}")

    @poll.command(aliases=['c'])
    async def create(self, ctx, *args):
        '''
        Creates a new poll

        usage: poll create YOUR POLL NAME : VALUE1 : VALUE2 : VALUE3 : ... : VALUEN
        '''
        params = ' '.join(args).split(' : ')

        if len(params) < 3:
            # Raise exception not enough parameters
            return

        pollName = params[0]
        pollValues = dict.fromkeys(params[1:], 0)

        if not self.polls.get(pollName):
            self.polls.update(
                {pollName: {
                    "values": pollValues,
                    "alreadyVoted": []
                }})
        else:
            # TODO if the poll exists then show a message
            pass

    @poll.command(aliases=['v'])
    async def vote(self, ctx, *args):

        if not args:
            # Raise exception no arguments Display help for vote
            pass

        params = ' '.join(args).split(' : ')

        # Ensure that there are exactly two parameters (poll name and vote)
        if len(params) == 2:
            # Raise exception Incorrect parameters
            pass

        poll = self.polls.get(params[0])
        vote = params[1]

        if not poll:
            # Raise exception poll does not exist
            pass

        if ctx.author.id not in poll.get("alreadyVoted"):
            poll.get("values")[vote] += 1
            poll.get("alreadyVoted").append(ctx.author.id)
        else:
            # TODO tell user they have already voted
            # Maybe we can allow them to switch the vote
            pass
        #print(self.polls)

    @poll.command(aliases=['s'])
    async def stats(self, ctx, *args):
        '''View statistics for polls'''

        if not args:
            all_poll_stats = [
                self._generate_pretty_poll(poll_name, self.polls.get(poll_name))
                for poll_name in self.polls
            ]

            sep = "\n"
            await ctx.message.channel.send(f"{sep.join(all_poll_stats)}")
        else:
            poll_name = ' '.join(args)
            pretty_poll_text = self._generate_pretty_poll(
                poll_name, self.polls.get(poll_name))
            await ctx.message.channel.send(pretty_poll_text)

    @create.error
    @list.error
    @poll.error
    @stats.error
    @vote.error
    async def music_cmd_error(self, ctx, error):
        await self.handle_command_error(ctx, error)

    def _generate_pretty_poll(self, poll_name, poll):
        '''
        Creates a pretty formatted string for the poll and its associated values.

        params:
            poll_name - A string which contains the name of the poll
            poll - A dictionary which contains the poll and all its associated data.
        '''
        pretty_poll = [f"```", poll_name]
        totals = poll.get("values")
        for key in totals.keys():
            pretty_poll.append(f"   {key} : {totals[key]}")
        pretty_poll.append("```")

        sep = "\n"
        pretty_poll = sep.join(pretty_poll)

        return pretty_poll
