from discord import app_commands
import discord
import pickledb
from discord.ext import commands
import sys
from Bard import Chatbot

# add ".." as a valid directory more info below
sys.path.append('..')

# while this shows up as an error, it isn't, since we are putting ".." into pythons list of active directories it actually knows log exists.
from log import log, level  # NOQA  -- ignore bc ^


# all cogs inherit from this base class
class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # adding a bot attribute for easier access
        with open("./bard.secret", "r") as sf:
            self.chatBot = Chatbot(f"{sf.read()}")
        self.db = pickledb.load("./discord.db", True)


    @commands.command(name="send")
    async def send_Command(self, ctx: commands.Context, *, args):

        author = str(ctx.author)
        if not self.db.exists(author):
            self.db.set(f"{author}.PRETENSE", "")
        pretense = self.db.get(f"{author}.PRETENSE")

        response = self.chatBot.ask(f"{pretense} {args}")
        msg = f"{ctx.author.mention}'s response to \"{args}\" with pretense: \"{pretense}\" is:\n{response['content']}"
        if len(msg) > 2000:
            msgs = [msg[i:i+1995] for i in range(0, len(msg), 1995)]
            for msg in msgs:
                await ctx.send(msg)
            return
        await ctx.send(msg)


    @commands.command(name="pretense")
    async def pretense_Command(self, ctx: commands.Context, *, args):
        pretense = args

        author = str(ctx.author)
        if not self.db.exists(f"{author}.PRETENSE"):
            self.db.set(f"{author}.PRETENSE", "")
        self.db.set(f"{author}.PRETENSE", f"{pretense}\n")

        await ctx.send(f"{ctx.author.mention} I have sent your pretense to \"{pretense}\". This pretense will only work for you.")

    @commands.command(name="check_pretense")
    async def pretense_check_Command(self, ctx: commands.Context):
        author = str(ctx.author)
        if not self.db.exists(f"{author}.PRETENSE"):
            self.db.set(f"{author}.PRETENSE", "")

        await ctx.send(f"{ctx.author.mention} Your pretense is currently: {self.db.get(f'{author}.PRETENSE')}")

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
    await bot.add_cog(AICog(bot=bot))
