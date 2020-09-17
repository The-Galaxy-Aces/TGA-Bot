import discord
import logging
import json
from time import localtime, strftime, sleep

from bot.features.insult import Insult


class Bot(discord.Client):
    def __init__(self, name, configFile):
        """The Bot class.
        The bot can do lots of neat things
        """
        super().__init__()

        self.name = ""
        self.token = ""
        self.configDict = {}
        self.features = {}

        #Logging setup
        self.log = logging.getLogger(name + 'Logger')
        #TODO make the logging level configurable at init
        self.log.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(
            filename='discordBot-' + name + "-" +
            strftime("%Y-%m-%d", localtime()) + ".log")
        self.handler.setFormatter(
            logging.Formatter(
                '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.log.addHandler(self.handler)

        self.process_config(configFile)
        print("\nStarting up " + self.name + "!\n")

        self.enable_features()

        self.log.info("Bot initalized")

    def process_config(self, configFile):
        with open(configFile, "r") as file:
            self.configDict = json.load(file)
        self.name = self.configDict["bot_name"]
        self.token = self.configDict["token"]
        if self.token == "Your Discord API Key" or not self.token:
            print("ERROR: No API Key. Please configure in config.json")
            self.log.error("No API Key. Please configure in config.json")

    def enable_features(self):

        print("Enabled features:")
        for x in self.configDict["enabled_features"]:
            if self.configDict["enabled_features"][x]["enabled"] == "True":
                self.features[x] = "True"
                print(f'\t{x}')
        print("")

    def set_logging_level(self, level):
        if level in [
                logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING,
                logging.ERROR, logging.CRITICAL
        ]:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.error("Bot.set_logging_level: Invalid logging level: " +
                           level)

    def get_token(self):
        return self.token

    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self))

    async def on_message(self, message):
        try:
            if message.author == self.user:
                return
            if self.features["insults"] and message.content.startswith(
                    "!insult"):
                i = Insult()
                for x in message.mentions:
                    self.log.info(x)
                    await message.channel.send(x.mention + i.getInsult())
                    sleep(1)
        except Exception as err:
            print(err)
            self.log.error(err)
