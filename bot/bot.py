import os
import json
import logging
import discord.ext
from time import localtime, strftime, sleep

from bot.features.insult import Insult


class Bot(discord.ext.commands.Bot):
    """
    The Bot class.
    The bot can do lots of neat things
    """

    def __init__(self, config_file):
        command_prefix = "."
        super().__init__(command_prefix)

        # Check for config file
        if not os.path.exists(config_file):
            raise OSError(f"{config_file} not found or missing")

        # Read in config file
        with open(config_file, 'r') as config_json:
            config = json.load(config_json)

        # Check bot for minimal required params to make bot run properly
        required_params = ['bot_name', 'token']
        missing_params = [param for param in required_params if not config.get(param)]
        if missing_params:
            raise AssertionError(f"config.json missing {missing_params}")

        # Pull information out of parsed config file
        self.name = config.get('bot_name')
        self.token = config.get('token')
        self.enabled_features = config.get('enabled_features')
        self.logging = config.get('logging')

        # Logging setup
        if bool(self.logging['enabled']):
            FORMAT = "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
            DATE_STAMP = strftime("%Y-%m-%d", localtime())
            FILE_NAME = f"discordBot-{self.name}-{DATE_STAMP}.log"

            self.log = logging.getLogger(f"{self.name} Logger")
            self.log.setLevel(config['logging']['logging_level'])
            self.handler = logging.FileHandler(filename=FILE_NAME)
            self.handler.setFormatter(logging.Formatter(FORMAT))
            self.log.addHandler(self.handler)

            self.log.info("Bot initalized")

        # Features
        self.listEnabledFeatures()
        self.add_cog(Insult(self))

    def listEnabledFeatures(self):
        print("Enabled features:")
        for enabled_feature in self.enabled_features:
            if bool(self.enabled_features[enabled_feature]["enabled"]):
                print(f"{enabled_feature}")
        print()

    def get_token(self):
        return self.token
