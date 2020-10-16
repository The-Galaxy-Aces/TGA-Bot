from discord.ext import commands


class TGACog(commands.Cog):
    def __init__(self, bot):
        raise AssertionError("TGACog should not be called.")

    def process_config(self, bot, REQUIRED_PARAMS):

        self.CONFIG = bot.enabled_features[self.__class__.__name__.lower()]

        MISSING_PARAMS = [
            param for param in REQUIRED_PARAMS if not self.CONFIG.get(param)
        ]
        if MISSING_PARAMS:
            raise AssertionError(f"config.yaml missing {MISSING_PARAMS}")

    def enable_cog(self):
        self.bot.log.debug(f"Enable Cog {self.__class__.__name__.lower()}")
        self.bot.add_cog(self)

    def disable_cog(self):
        self.bot.log.debug(f"Disable Cog {self.__class__.__name__.lower()}")
        self.bot.remove_cog(self)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.name} {self.__class__.__name__.lower()} is ready!")
        self.ready = True
