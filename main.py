from bot.bot import Bot


def main():

    print("Starting up The Galaxy Aces Bot!")

    bot = Bot("TGA", "config.json")
    bot.run(bot.getToken())


main()
