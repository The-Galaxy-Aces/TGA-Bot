import threading
import asyncio
from time import sleep


class TGACli:
    def __init__(self, bots, OSTYPE):
        self.OSTYPE = OSTYPE
        self.bots = bots

        self.cmdMap = {"quit": 0, "exit": 0, "q": 0, "test": 1}

        self.switcher = {0: lambda: self.quit(), 1: lambda: self.test()}

        self.thread = threading.Thread(target=self.inputLoop, args=())

        self.thread.start()

    def inputLoop(self):
        # Wait for the bots to be ready
        while (True):
            cmd = input(">>> ")
            self.parseCommand(cmd)

    def parseCommand(self, cmd):

        try:
            cmdList = cmd.split()
            #print(f"You are running the cmd: {cmd}")
            #print(f"Your command list: {cmdList}")
            if cmdList[0].lower() in self.cmdMap:
                self.switcher.get(self.cmdMap.get(cmdList[0].lower()))()

        except Exception as e:
            print(e)

    def quit(self):
        print("Exiting")
        for bot in self.bots:
            bot.loop.stop()
            bot.thread.join()
            bot.loop.close()
        exit(0)

    def test(self):
        print("test")
