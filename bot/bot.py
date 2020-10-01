import os
import json
import logging
import discord
import discord.ext
from time import localtime, strftime, sleep

from bot.features.insult import Insult


class Bot(discord.ext.commands.Bot):
    """
    The Bot class.
    The bot can do lots of neat things
    """
    def __init__(self, CONFIG):

        # Check bot for minimal required params to make bot run properly
        REQUIRED_PARAMS = ['bot_name', 'token', 'command_prefix']
        MISSING_PARAMS = [
            param for param in REQUIRED_PARAMS if not CONFIG.get(param)
        ]
        if MISSING_PARAMS:
            raise AssertionError(f"config.yaml missing {MISSING_PARAMS}")

        # Pull information out of parsed config file
        self.name = CONFIG.get('bot_name')
        self.token = CONFIG.get('token')
        self.command_prefix = CONFIG.get('command_prefix')
        self.enabled_features = CONFIG.get('enabled_features')
        self.logging = CONFIG.get('logging')

        super().__init__(self.command_prefix)

        # Logging setup
        if self.logging['enabled'] == "True":
            FORMAT = "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
            DATE_STAMP = strftime("%Y-%m-%d", localtime())
            FILE_NAME = f"discordBot-{self.name}-{DATE_STAMP}.log"

            self.log = logging.getLogger(f"{self.name} Logger")
            self.log.setLevel(CONFIG['logging']['logging_level'])
            self.handler = logging.FileHandler(filename=FILE_NAME)
            self.handler.setFormatter(logging.Formatter(FORMAT))
            self.log.addHandler(self.handler)

            self.log.info("Bot initalized")

        # Features
        self.listEnabledFeatures()
        self.add_cog(Insult(self))

    def listEnabledFeatures(self):
        print(f"{self.name} Enabled Features:")
        for enabled_feature in self.enabled_features:
            if self.enabled_features[enabled_feature]["enabled"] == "True":
                print(f"\t{enabled_feature}")
        print()

    def get_token(self):
        return self.token
