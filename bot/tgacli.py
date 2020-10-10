import threading
import asyncio
from time import sleep


class TGACli:
    '''
    The Galaxy Aces Discord Bot CLI Interface
    quit exit q - Closes the bots and exits the program.
    list - lists the avaiable bots.
    select <bot_id> - Selects the <bot_id> for further commands.
    help - Displays this help
    '''
    def __init__(self, bots, OSTYPE):
        '''
        Initalize TGADB CLI Interface
        '''

        self.OSTYPE = OSTYPE
        self.bots = bots
        self.activeBot = 0
        self.exit = False
        self.ready = False

        # The
        self.cmdMap = {
            "e": 0,
            "exit": 0,
            "q": 0,
            "quit": 0,
            "h": 1,
            "help": 1,
            "l": 2,
            "list": 2,
            "s": 3,
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
        while (not self.ready):
            if all(all(cog.ready for cog in bot.cogList) for bot in self.bots):
                self.ready = True
            else:
                sleep(1)
            """ for bot in self.bots:
                if all(bot.is_ready() != True for bot in self.bots) and all(cog.ready != True for cog in bot.cogList):
                    # if all(bot.is_ready() != True for bot in self.bots) and
                    sleep(0.5)
                else:
                    self.ready = True """

        while (not self.exit):
            activeBotName = self.bots[self.activeBot].name
            cmd = input(f"\n{activeBotName}: >>> ")
            self.parseCommand(cmd)
        print("InputLoopFinished")

    def parseCommand(self, cmd):

        if cmd:
            try:
                cmdList = cmd.split()
                if cmdList[0].lower() in self.cmdMap:
                    self.commandCall.get(self.cmdMap.get(cmdList[0].lower()))(
                        cmdList[1:])
            except Exception as e:
                print(e)

    def quit(self, cmd):
        '''
        Exit the CLI Interface and shut down all running bots.
        '''
        print("Exiting")
        for bot in self.bots:
            bot.loop.stop()
            bot.thread.join()

            if not bot.loop.is_closed():
                bot.loop.close()

            print(f"{bot.name} shutdown.")
        self.exit = True
        exit(0)

    def list(self, cmd):
        '''
        Lists all the avaiable bots.
        '''
        for bot in self.bots:
            print(f"{bot.bot_id}\t{bot.name}")

    def select(self, cmd):
        '''
        Selects a particular bot to perform actions on.
        '''
        if not cmd:
            print("Enter a bot_id to select that bot for further commands.")
            self.list(cmd)
            return

        bot_selection = cmd[0]
        if bot_selection and bot_selection.isdigit(
        ) and int(bot_selection) <= len(self.bots):
            self.activeBot = int(bot_selection) - 1
        else:
            print(
                f"{bot_selection} is an invalid selection. Please select a valid bot_id:"
            )
            self.list(cmd)

    def help(self, cmd):
        '''
        Displays this help menu.
        '''
        print("\n")
        if not len(cmd):
            help(self)
        else:
            help(getattr(self, cmd[0], lambda: print("Function not found")))
