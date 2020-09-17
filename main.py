from bot.bot import Bot


def main():

    bot = Bot("TGA", "config.json")
    bot.run(bot.get_token())


main()
