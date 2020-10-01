import os
import threading
import asyncio
import yaml
import sys
from bot.bot import Bot


async def threadedBot(bot):
    await bot.start(bot.get_token())


def loopTheBot(loop):
    if not loop.is_running():
        loop.run_forever()


def main():

    config_file = "config.yaml"

    # Check for config file
    if not os.path.exists(config_file):
        raise OSError(f"{config_file} not found or missing")

    # Read in config file
    with open(config_file, 'r') as config_yaml:
        CONFIG = yaml.full_load(config_yaml)

    for botConfig in CONFIG["bots"]:
        if sys.version_info[0] == 3 and sys.version_info[
                1] >= 8 and sys.platform.startswith('win'):
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())
        else:
            asyncio.get_child_watcher()

        loop = asyncio.get_event_loop()

        bot = Bot(botConfig["config"])
        loop.create_task(threadedBot(bot))

        thread = threading.Thread(target=loopTheBot, args=(loop, ))
        thread.start()


if __name__ == "__main__":
    main()
