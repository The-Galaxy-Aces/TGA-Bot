import os
import threading
import asyncio
import yaml
import signal
import sys
from time import sleep
from bot.bot import Bot


async def threadedBot(bot):
    await bot.start(bot.get_token())


def loopTheBot(loop):
    if not loop.is_running():
        loop.run_forever()


def main():
    def signal_handler(
        sig,
        frame,
    ):
        sys.exit(0)

    bots = []
    config_file = "config.yaml"

    # May replace with with platform.system() later
    osType = 'win' if sys.version_info[0] == 3 and sys.version_info[
        1] >= 8 and sys.platform.startswith('win') else 'linux'

    # Check for config file
    if not os.path.exists(config_file):
        raise OSError(f"{config_file} not found or missing")

    # Read in config file
    with open(config_file, 'r') as config_yaml:
        CONFIG = yaml.full_load(config_yaml)

    for botConfig in CONFIG["bots"]:
        if osType == 'win':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())
        else:
            asyncio.get_child_watcher()

        loop = asyncio.get_event_loop()

        bot = Bot(botConfig["config"])
        bots.append(bot)
        loop.create_task(threadedBot(bot))

        thread = threading.Thread(target=loopTheBot,
                                  args=(loop, ),
                                  daemon=True)
        thread.start()

    # Properly handle the control+c
    signal.signal(signal.SIGINT, signal_handler)

    # signal.pause() is not available on windows so just do an endless loop
    # The pause and loop is needed for now since the threads above were set to daemon
    # and will be terminated when the main program exits
    if osType == 'win':
        while (True):
            sleep(1)
    else:
        signal.pause()


if __name__ == "__main__":
    main()
