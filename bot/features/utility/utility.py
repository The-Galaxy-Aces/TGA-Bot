import random
from discord.ext import commands
from bot.features.tgacog import TGACog
import pprint


class Utility(TGACog):
    '''
    Assorted utility commands
    '''
    def __init__(self, bot):
        super().__init__(bot)

        REQUIRED_PARAMS = []
        self.process_config(self.bot, REQUIRED_PARAMS)

    async def _generate_context_from_payload(self, payload):
        # Get the channel the message was edited in.
        channel = self.bot.get_channel(int(payload.data["channel_id"]))

        # Get the entire message from the channel.
        message = await channel.fetch_message(payload.message_id)

        # Return the context
        return await self.bot.get_context(message)

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):

        # Get the edited text from the message.
        content = payload.data.get('content')

        if content.strip().startswith(self.bot.command_prefix):

            ctx = await self._generate_context_from_payload(payload)

            args = content.lstrip(self.bot.command_prefix).split()

            cog_commands = self.get_commands()

            pprint.pprint(f"commands: {cog_commands}")

            # Execute as a group
            if isinstance(cog_commands[0], commands.core.Group):

                command_set = cog_commands[0].commands

                while command_set:
                    command = command_set.pop()

                    print(f"command: {command}")
                    print(f"command: {type(command)}")

                # for command in command_set:
                # print(command.name)
                '''print(f"name: {cog_commands[0].name}")
                print(f"aliases: {cog_commands[0].aliases}")
                print(f"commands: {cog_commands[0].commands.pop()}")
                print(f"full_parent_name: {cog_commands[0].full_parent_name}")
                print(f"clean_params: {cog_commands[0].clean_params}")
                print(f"parents: {cog_commands[0].parents}")
                print(f"qualified_name: {cog_commands[0].qualified_name}")
                print(f"root_parent: {cog_commands[0].root_parent}")
                print(f"signature: {cog_commands[0].signature}")'''

                command = f"{args[0]} {args[1]}"

                await self.bot.get_command(command).callback(
                    self, ctx, args[2])
            else:
                pass
                # Execute as a command

    @commands.group(aliases=['u'])
    @TGACog.check_permissions()
    async def utility(self, ctx):
        '''
        Assorted utility commands
        '''
        pass

    @utility.command(aliases=['r'])
    @TGACog.check_permissions()
    async def roll(self, ctx, *args):
        '''
        Roll integer - a random value between 0 and your entered value.
        If no value is entered the roll will be between 0 and 100 inclusive.
        '''

        try:
            roll = int(args[0]) if args else 100

            if roll > 0:
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
            await ctx.message.channel.send(f'An unknown error occured: {e}')

    @utility.error
    @roll.error
    async def utility_cmd_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send(
                f"Error in {self.__class__.__name__}: {error}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.channel.send(
                "You do not have permissions to use that command.")
