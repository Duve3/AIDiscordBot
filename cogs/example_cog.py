from discord import app_commands
import discord
from discord.ext import commands
import sys

# add ".." as a valid directory more info below
sys.path.append('..')

# while this shows up as an error, it isn't, since we are putting ".." into pythons list of active directories it actually knows log exists.
from log import log, level  # NOQA  -- ignore bc ^


# all cogs inherit from this base class
class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # adding a bot attribute for easier access

    # adding a command to the cog
    @commands.command(name="ping")
    async def pingcmd(self, ctx):
        """the best command in existence"""
        await ctx.send(ctx.author.mention)

    # adding a slash command to the cog (make sure to sync this!)
    @app_commands.command(name="ping", description="Replies with pong (sometimes?)")
    async def slash_pingcmd(self, interaction):
        """the second-best command in existence"""
        await interaction.response.send_message(interaction.user.mention)

    @commands.command(name="test")
    async def test(self, ctx):
        messageStuff = ctx.message.content.split(" ")
        messageStuff.pop(0)
        print(messageStuff)
        await ctx.channel.send("This is a test command.")

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
    await bot.add_cog(ExampleCog(bot=bot))
