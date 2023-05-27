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
            result = sf.read()
            if result is None or result == "":
                log("discord.AI_cog.__init__", "FAILED TO LOAD AI INFORMATION, EXITING...", level.ERROR)
                exit(-1)
            try:
                self.chatBot = Chatbot(f"{result}")
            except AttributeError as e:
                log("discord.AI_cog.__init__", "FAILED TO LOAD AI INFORMATION, EXITING...\n(THIS IS A MAJOR ERROR, REPORT ON THE GITHUB PAGE NOW)", level.ERROR)
                log("discord.AI_cog.__init__", f"ERROR EXTRACTED: {repr(e)}", level.INFO)
                exit(-1)  # return doesn't work in this case as __init__ is supposed to return nothing anyway.
        self.db = pickledb.load("./discord.db", True)


    @commands.hybrid_command(name="send", with_app_command=True)
    async def send_Command(self, ctx: commands.Context, *, args):
        await ctx.defer()  # this process can take longer than the 3 seconds given, especially with lower end servers/systems
        author = str(ctx.author)
        if not self.db.exists(f"{author}.PRETENSE"):
            self.db.set(f"{author}.PRETENSE", "")
        pretense = self.db.get(f"{author}.PRETENSE")

        response = self.chatBot.ask(f"{pretense} {args}")
        normal_pretense = str.strip(pretense, "\n")
        p_text = f" with pretense: \"{normal_pretense}\"" if normal_pretense != "" else ""
        msg = f"Response to \"{args}\"{p_text} is:\n{response['content']}"
        if len(msg) > 2000:
            msgs = [msg[i:i+1995] for i in range(0, len(msg), 1995)]
            for msg in msgs:
                await ctx.send(msg)
            return

        await ctx.reply(msg)


    @commands.hybrid_command(name="pretense", with_app_command=True)
    async def pretense_Command(self, ctx: commands.Context, *, args):
        await ctx.defer()  # this process can take longer than the 3 seconds given, especially with lower end servers/systems
        log("discord.client.AI_cog.pretense_Command", f"Running pretense command with {args}", level.DEBUG)
        pretense = args

        author = str(ctx.author)
        if not self.db.exists(f"{author}.PRETENSE"):
            self.db.set(f"{author}.PRETENSE", f"{pretense}\n")
        self.db.set(f"{author}.PRETENSE", f"{pretense}\n")

        await ctx.reply(f"I have sent your pretense to \"{pretense}\". This pretense will only work for you.")

    @commands.command(name="check_pretense")
    async def pretense_check_Command(self, ctx: commands.Context):
        author = str(ctx.author)
        if not self.db.exists(f"{author}.PRETENSE"):
            self.db.set(f"{author}.PRETENSE", "")

        await ctx.reply(f"Your pretense is currently: {self.db.get(f'{author}.PRETENSE')}")

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
