from bot.bot import Bot


def main():

    bot = Bot("config.json")
    bot.run(bot.get_token())


if __name__ == "__main__":
    main()
