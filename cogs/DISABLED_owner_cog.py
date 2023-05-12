from discord import app_commands
import discord
from discord.ext import commands
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


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sync")
    async def sync(self, ctx):
        messageStuff = ctx.message.content.split(" ")
        messageStuff.pop(0)
        if ctx.author.id == 680116696819957810:
            if len(messageStuff) != 0:
                log("discord.Client.app_commands.Sync", f"Syncing app commands to {ctx.message.guild.id}", level.INFO)
                await ctx.channel.send("Syncing app commands to this guild!")
                await self.bot.tree.sync(guild=discord.Object(ctx.message.guild.id))
                await ctx.channel.send("Successfully synced app commands to this guild!")
            else:
                log("discord.Client.app_commands.Sync", "Owner has asked to sync, awaiting confirmation.", level.INFO)
                await ctx.channel.send("Are you sure you want to sync app commands GLOBALLY? This process can take up to an hour!")
                msg = await self.bot.wait_for('message', check=check, timeout=30)
                if isATypeOfYes(msg. content):
                    log("discord.Client.app_commands.Sync", f"Syncing app commands globally", level.INFO)
                    await ctx.channel.send("Syncing app commands globally, can take up to an hour.")
                    await self.bot.tree.sync()
                else:
                    log("discord.Client.app_commands.Sync", f"Owner denied sync.", level.INFO)
                    await ctx.channel.send("No longer syncing app commands globally. \nIf your trying to sync at a guild level check your goofy code.")
        else:
            await ctx.channel.send('You must be the owner to use this command!')

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
    await bot.add_cog(OwnerCog(bot=bot))
