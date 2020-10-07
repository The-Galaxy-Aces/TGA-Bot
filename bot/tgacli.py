import threading
import asyncio
from time import sleep


class TGACli:
    def __init__(self, bots, OSTYPE):
        self.OSTYPE = OSTYPE
        self.bots = bots
        self.activeBot = 0

        # The
        self.cmdMap = {
            "quit": 0,
            "exit": 0,
            "q": 0,
            "help": 1,
            "list": 2,
            "select": 3
        }

        self.commandCall = {
            0: lambda x: self.quit(x),
            1: lambda x: self.help(x),
            2: lambda x: self.list(x),
            3: lambda x: self.select(x)
        }

        self.thread = threading.Thread(target=self.inputLoop, args=())

        self.thread.start()

    def inputLoop(self):
        # Wait for the bots to be ready
        while (True):
            cmd = input(f"{self.bots[self.activeBot].name}: >>> ")
            self.parseCommand(cmd)

    def parseCommand(self, cmd):

        try:
            cmdList = cmd.split()
            # print(f"You are running the cmd: {cmd}")
            # print(f"Your command list: {cmdList}")
            if cmdList[0].lower() in self.cmdMap:
                self.commandCall.get(self.cmdMap.get(cmdList[0].lower()))(
                    cmdList[1:])
        except Exception as e:
            print(e)

    def quit(self, cmd):
        print("Exiting")
        for bot in self.bots:
            bot.loop.stop()
            bot.thread.join()
            bot.loop.close()
            print(f"{bot.name} shutdown.")
        exit(0)

    def list(self, cmd):
        for bot in self.bots:
            print(f"{bot.bot_id}\t{bot.name}")

    def select(self, cmd):
        if not cmd:
            print("Enter a bot_id to select that bot for further commands.")
            self.list(cmd)

    def help(self, cmd):
        print("quit exit q - Closes the bots and exits the program.")
        print("list - lists the avaiable bots.")
        print("select <bot_id> - Selects the <bot_id> for further commands.")
        print("help - Displays this help")
        print('test')
