import os
import threading
import asyncio
import yaml
import signal
import sys
from bot.bot import Bot
from bot.tgacli import TGACli


def main():

    CONFIG_FILE = "config.yaml"
    OSTYPE = sys.platform

    async def threaded_bot(bot):
        await bot.start(bot.get_token())

    def loop_the_bot(loop):
        if not loop.is_running():
            loop.run_forever()

    def signal_handler(sig, frame):
        sys.exit(0)

    # Check for config file
    if not os.path.exists(CONFIG_FILE):
        raise OSError(f"{CONFIG_FILE} not found or missing")

    # Read in config file
    with open(CONFIG_FILE, 'r', encoding='UTF-8') as CONFIG_YAML:
        CONFIG = yaml.full_load(CONFIG_YAML)

    bots = []
    for bot_id, bot_config in enumerate(CONFIG, start=1):

        # Use enumeration as bot's ID
        bot_config.update({'bot_id': bot_id})

        bot = Bot(bot_config, OSTYPE)
        bot.loop = asyncio.get_event_loop()
        bot.loop.create_task(threaded_bot(bot))
        bot.thread = threading.Thread(
            target=loop_the_bot,
            args=[bot.loop],
            daemon=True
        )
        bot.thread.start()

        # Have an array of bots to feed to CLI
        bots.append(bot)

    # Setup the cli in its own thread
    TGACli(bots, OSTYPE)

    # Properly handle the control+c
    signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    main()
