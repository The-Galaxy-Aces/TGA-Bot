import os
import logging
import discord
import discord.ext
from time import localtime, strftime

from bot.features.insult.insult import Insult
from bot.features.music.music import Music


class Bot(discord.ext.commands.Bot):
    """
    The Bot class.
    The bot can do lots of neat things
    """
    def __init__(self, CONFIG, OSTYPE):

        self.CONFIG = CONFIG
        self.OSTYPE = OSTYPE
        self.cog_list = []
        self.thread = ""
        self.loop = ""

        # Check bot for minimal required params to make bot run properly
        REQUIRED_PARAMS = [
            'bot_id', 'command_prefix', 'enabled_features', 'logging', 'name',
            'token'
        ]
        MISSING_PARAMS = [
            param for param in REQUIRED_PARAMS if not CONFIG.get(param)
        ]
        if MISSING_PARAMS:
            raise AssertionError(f"config.yaml missing {MISSING_PARAMS}")

        # Pull information out of parsed config file
        self.bot_id = CONFIG.get('bot_id')
        self.command_prefix = CONFIG.get('command_prefix')
        self.enabled_features = CONFIG.get('enabled_features')
        self.logging = CONFIG.get('logging')
        self.name = CONFIG.get('name')
        self.token = CONFIG.get('token')

        super().__init__(self.command_prefix)

        if self.logging:
            self.setup_logging()

        self.enable_features()

        self.log.info("Bot initalized")

    def setup_logging(self):
        # Logging setup
        try:
            if self.OSTYPE == "win32":
                log_path = "logs"
            else:
                log_path = f"{os.sep}var{os.sep}log{os.sep}discord_bot"

            os.mkdir(log_path)
        except FileExistsError:
            pass
        except Exception as e:
            raise AssertionError(
                f"logs directory was not able to be created for some reason: {e}"
            )

        FORMAT = "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
        DATE_STAMP = strftime("%Y-%m-%d", localtime())
        FILE_NAME = f"{log_path}{os.sep}discord_bot-{self.name}-{DATE_STAMP}.log"

        self.log = logging.getLogger(f"{self.name} Logger")
        self.log.setLevel(self.CONFIG['logging']['logging_level'])
        self.handler = logging.FileHandler(filename=FILE_NAME)
        self.handler.setFormatter(logging.Formatter(FORMAT))
        self.log.addHandler(self.handler)

    def enable_features(self):
        print(f"{self.name} enabled features:", end="\n")
        for feature in self.enabled_features:
            if self.enabled_features[feature]["enabled"]:
                cog = getattr(
                    self, f"get_{feature}", lambda: (_ for _ in ()).throw(
                        Exception(
                            f"Feature {feature} does not exist. Review config.yaml"
                        )))()
                self.cog_list.append(cog)
                self.cog_list[-1].enable_cog()
                print(f'  {feature}')
        print("")

    def get_token(self):
        return self.token

    def get_music(self):
        return Music(self)

    def get_insult(self):
        return Insult(self)
