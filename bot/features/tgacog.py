from discord.ext import commands

class TGACog(commands.Cog):
    def __init__(self, bot):
        self.COG_NAME = self.__class__.__name__.lower()
        self.CONFIG = bot.enabled_features[self.COG_NAME]

        self.bot = bot
        self.ready = False
        self.enabled = False
        self._last_member = None
        self.permissions = self.CONFIG.get("permissions")

    def _process_config(self, REQUIRED_PARAMS):
        """
        Checks supplied REQUIRED_PARAMS against self.CONFIG.
        Raises an AssertionError if config is missing anything from required
        params.
        """
        MISSING_PARAMS = [
            param for param in REQUIRED_PARAMS if not self.CONFIG.get(param)
        ]

        if MISSING_PARAMS:
            raise AssertionError(f"config.yaml missing {MISSING_PARAMS}")

    def _toggle_cog(self):
        """
        Adds or removes itself accordingly. This is determined by a reference
        to self.enabled.
        """
        self.enabled = not self.enabled
        disable_enable = ["Disable", "Enable"][self.enabled]
        self.bot.log.info(f"{disable_enable} Cog {self.COG_NAME}")
        self.bot.add_cog(self) if self.enabled \
            else self.bot.remove_cog(self.COG_NAME.title())

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Prints & sets self.ready to True when cog is ready.
        """
        self.ready = True
        print(f"{self.bot.name} {self.COG_NAME} is ready!")

    async def _handle_command_error(self, ctx, error):
        """
        Handles error messaging depending on the type of error provided.
        """
        if isinstance(error, commands.BadArgument):
            await ctx.message.channel.send(
                f"Error in {self.COG_NAME}: {error}")
        elif isinstance(error, commands.CheckFailure):
            await ctx.message.channel.send(
                "You do not have permissions to use that command.")
        else:
            self.bot.log.error(f"handle_command_error: {error}")

def check_permissions():
    async def predicate(ctx):
        command_name = ctx.invoked_subcommand.name \
            if ctx.invoked_subcommand else ctx.command.name
        cmd_permissions = ctx.cog.permissions.get(command_name)

        return any(role for role in ctx.author.roles
                    if role.name in cmd_permissions)

    return commands.check(predicate)
