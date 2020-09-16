import discord
import logging
import json
from time import localtime, strftime, sleep

from bot.features.insult import Insult


class Bot(discord.Client):
    def __init__(self, name, configFile):
        super().__init__()

        self.name = name
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

        self.log.info("Bot initalized")

    def process_config(self, configFile):
        with open(configFile, "r") as file:
            self.configDict = json.load(file)
        self.token = self.configDict["token"]
        self.enable_features()

    def enable_features(self):

        print("Enabled features:")
        for x in self.configDict["enabled_features"]:
            if self.configDict["enabled_features"][x]["enabled"] == "True":
                self.features[x] = "True"
                print(f'\t{x}')
        print("")

    def setLoggingLevel(self, level):
        if level in [
                logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING,
                logging.ERROR, logging.CRITICAL
        ]:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.error(__self__.method.__qualname +
                           "Invalid logging level: " + level)

    def getToken(self):
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
