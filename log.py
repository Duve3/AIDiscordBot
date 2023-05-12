import datetime
import os

from colors import ColorsClass
import logging

date = datetime.date.today()
date = date.strftime("%Y-%d-%m")
if not os.path.exists("./logs/"):
    os.mkdir("./logs/")

logging.basicConfig(filename=f'./logs/{date}.log', filemode='a', format="%(asctime)s %(name)-30s %(levelname)-8s %(message)s", datefmt='%Y-%d-%m %H:%M:%S', level="DEBUG")
color = ColorsClass()
levelRange = {
    0: "DEBUG    ",
    1: "INFO     ",
    2: "WARNING  ",
    3: "ERROR    "
}


# I just need the callable objects of a class to make it simpler
class ClassLevelRanges:
    def __init__(self):
        self.DEBUG = 0
        self.INFO = 1
        self.WARNING = 2
        self.ERROR = 3


level = ClassLevelRanges()


def log(clientType, message, level=0):
    if level not in levelRange.keys():
        return

    now = datetime.datetime.now()
    time = now.strftime("%Y-%d-%m %H:%M:%S")
    logString = f"{color.BLACK}{time} {color.LIGHT_BLUE}{levelRange[level]}{color.PURPLE}{clientType} {color.RED}{message}{color.ENDC}"
    print(logString)
    data = {'user': f'CL.{clientType}'}
    if level == 0:
        logging.debug(message, extra=data)
    elif level == 1:
        logging.info(message, extra=data)
    elif level == 2:
        logging.warning(message, extra=data)
    elif level == 3:
        logging.error(message, extra=data)


log("CustomLogger (CL)", "CustomLogger has sucessfully loaded!", 1)

if __name__ == "__main__":
    log("discord.client", "Test", 1)
    log("discord.client", "Test", 2)
    log("discord.client", "Test", 0)
    log("discord.client", "Test", 3)
