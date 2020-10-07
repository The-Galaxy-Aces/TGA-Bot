import os
import threading
import asyncio
import yaml
import signal
import sys
from time import sleep
from bot.bot import Bot
from bot.tgacli import TGACli


async def asyncInputLoop(func):
    return await asyncio.coroutine(func)()


def inputLoop(*args):

    while (True):
        cmd = input(">>> ")
        print(cmd)


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
    OSTYPE = 'win' if sys.version_info[0] == 3 and sys.version_info[
        1] >= 8 and sys.platform.startswith('win') else 'linux'

    # Check for config file
    if not os.path.exists(config_file):
        raise OSError(f"{config_file} not found or missing")

    # Read in config file
    with open(config_file, 'r') as config_yaml:
        CONFIG = yaml.full_load(config_yaml)

    for botConfig in CONFIG["bots"]:
        if OSTYPE == 'win':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())
        else:
            asyncio.get_child_watcher()

        loop = asyncio.get_event_loop()

        bot = Bot(botConfig["config"], OSTYPE)
        loop.create_task(threadedBot(bot))

        thread = threading.Thread(target=loopTheBot,
                                  args=(loop, ),
                                  daemon=True)
        bot.thread = thread
        bot.loop = loop
        bots.append(bot)
        thread.start()

    # Setup the cli in its own thread
    cli = TGACli(bots, OSTYPE)

    # Properly handle the control+c
    signal.signal(signal.SIGINT, signal_handler)

    # signal.pause() is not available on windows so just do an endless loop
    # The pause and loop is needed for now since the threads above were set to daemon
    # and will be terminated when the main program exits
    if OSTYPE == 'win':
        while (True):
            sleep(1)
    else:
        signal.pause()


if __name__ == "__main__":
    main()
