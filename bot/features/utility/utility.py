import random
from discord.ext import commands
from bot.features.tgacog import TGACog


class Utility(TGACog):
    '''
    Assorted utility commands
    '''
    def __init__(self, bot):
        super().__init__(bot)

        REQUIRED_PARAMS = []
        self.process_config(self.bot, REQUIRED_PARAMS)

    '''@commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # TODO Read the message and determine if it is a command we want to process.
        # This executes twice for some reason, going to try using on_raw_message_edit
        # Also because this will not trigger on edits made while the bot was not running
        # or if the bot was restarted, anything that was entered. raw_message_edit works on
        # everything
        print(f'edited {before.content}')'''

    async def _analyse_content(self, content):
        if content.startswith(self.bot.command_prefix):
            #           print(content)
            args = content.lstrip(self.bot.command_prefix).split()
            print(args[1])
            print(self.bot.get_command(args[1]))
            await self.bot.invoke(self.bot.get_command(args[1]), args=args[2])
        else:
            return False

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):

        content = payload.data.get('content')

        if await self._analyse_content(content):
            print('going to execute commands')

    @commands.group(aliases=['u'])
    @TGACog.check_permissions()
    async def utility(self, ctx):
        '''
        Assorted utility commands
        '''
        pass

    @utility.command(aliases=['r'])
    @TGACog.check_permissions()
    async def roll(self, ctx, args):
        '''
        Roll integer - a random value between 0 and your entered value.
        '''
        try:
            roll = int(args)
            if roll >= 0:
                await ctx.message.channel.send(
                    f"`{ctx.message.author.name} rolled a {random.randint(0,roll)}.`"
                )
            else:
                raise ValueError
        except ValueError:
            await ctx.message.channel.send(
                "Please enter an integer greater than or equal to 1 for your roll."
            )
        except Exception as e:
            await ctx.message.channel.send(f"An unknown error occured: {e}")

    @utility.error
    @roll.error
    async def utility_cmd_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send(
                f"Error in {self.__class__.__name__}: {error}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.channel.send(
                "You do not have permissions to use that command.")
