import discord
import logging
import json

from features.insult import Insult


def setup_logging():
    log = logging.getLogger('discord')
    log.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log',
                                  encoding='utf-8',
                                  mode='w')
    handler.setFormatter(
        logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    log.addHandler(handler)


def read_config():
    with open("config.json", "r") as file:
        configDict = json.load(file)

    return configDict


def enable_features(config):

    features = {}

    print("Enabled features:")
    for x in config["enabled_features"]:
        if config["enabled_features"][x]["enabled"] == "True":
            features[x] = "True"
            print(f'\t{x}')

    print("")

    return features


def main():

    print("Starting up The Galaxy Aces Bot!")

    setup_logging()

    config = read_config()

    token = config["token"]

    features = enable_features(config)

    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if features["insults"] and message.content.startswith("!insult"):
            i = Insult()
            for x in message.mentions:
                await message.channel.send(x.mention + i.getInsult())

    client.run(token)


main()
