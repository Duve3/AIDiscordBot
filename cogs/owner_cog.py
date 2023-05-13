from discord import app_commands
import discord
from discord.ext import commands
import sys

# add ".." as a valid directory more info below
sys.path.append('..')

# while this shows up as an error, it isn't, since we are putting ".." into pythons list of active directories it actually knows log exists.
from log import log, level  # NOQA  -- ignore bc ^


# all cogs inherit from this base class
class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # adding a bot attribute for easier access

    @commands.command(name="sync_tree")
    @commands.is_owner()
    async def sync_command(self, ctx: commands.Context, *, guildID=None):
        channel = ctx.channel
        author = ctx.author
        yesList = [
            "yes",
            "yeah",
            "ye",
            "y",
            "yea",
            "yep",
            "yeh"
        ]

        # check
        def check(m):
            return m.author == author and m.channel == channel and m.content.lower() in yesList

        if guildID is None:
            log("discord.client.owner_cog.sync_tree", "Attempting tree sync GLOBALLY, awaiting confirmation", level.DEBUG)
            await ctx.send("Are you sure you want to sync bot commands GLOBALLY?\nThis is possibly a destructive action!")

            confirmation = await self.bot.wait_for("message", check=check)
            if confirmation:
                log("discord.client.owner_cog.sync_tree", "Syncing command tree GLOBALLY.", level.INFO)
                await self.bot.tree.sync()
            else:
                log("discord.client.owner_cog.sync_tree", "Denied GLOBAL sync.", level.DEBUG)
                await ctx.send("Cancelled GLOBAL sync.")
        else:
            log("discord.client.owner_cog.sync_tree", f"Syncing tree on guild: {guildID}", level.DEBUG)
            await self.bot.tree.sync(guild=discord.Object(id=guildID))
        await ctx.send(f"Synced bot to {guildID if guildID is not None else 'GLOBAL'}")

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
