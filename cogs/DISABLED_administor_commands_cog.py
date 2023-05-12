from discord import app_commands
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
import sys

# add ".." as a valid directory more info below
sys.path.append('..')

# while this shows up as an error, it isn't, since we are putting ".." into pythons list of active directories it actually knows log exists.
from log import log, level  # NOQA  -- ignore bc ^


def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check


def isATypeOfYes(msg: str):
    typeOfYeses = [
        "yes",
        "y",
        "ye",
        "ya",
        "yah",
        "yea",
        "yeh",
        "yeah",
        "yessir"
    ]
    if msg.lower() in typeOfYeses:
        return True
    return False


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # doing something when the cog gets loaded
    async def cog_load(self):
        log(f"discord.Client.Cogs.{self.__class__.__name__}", f"{self.__class__.__name__} loaded!", level.DEBUG)

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        log(f"discord.Client.Cogs.{self.__class__.__name__}", f"{self.__class__.__name__} unloaded!", level.DEBUG)


# usually you’d use cogs in extensions
# you would then define a global async function named 'setup', and it would take 'bot' as its only parameter
async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(AdminCog(bot=bot))
