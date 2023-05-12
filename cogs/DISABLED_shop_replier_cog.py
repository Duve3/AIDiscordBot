from discord import app_commands
import discord
from discord.ext import commands
import sys

# add ".." as a valid directory more info below
sys.path.append('..')

# while this shows up as an error, it isn't, since we are putting ".." into pythons list of active directories it actually knows log exists.
from log import log, level  # NOQA  -- ignore bc ^

ChannelIDS = [1077416852323586090]


class ShopReplierCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.channel.id not in ChannelIDS:
            return

        if not message.attachments:
            return

        await message.add_reaction('🇼')
        await message.add_reaction('🇱')

        thread = await message.channel.create_thread(
            name=f"Is {message.author.display_name}'s shop a W or an L?",
            type=discord.ChannelType.public_thread,
            message=message,
            reason="Bot automatic thread creation"
        )

        await thread.send(f"Talk about {message.author.display_name}'s shop here!")

    @commands.command(name="addChannel")
    async def addChannel(self, ctx, channelID: int = 0):
        if ctx.message.author.id != 680116696819957810:
            await ctx.send(f"{ctx.message.author.mention} :gun:")
            return

        log("discord.Client.Cog.ShopReplierCog.addChannel", "Adding Channel to ChannelID list", level.INFO)
        if channelID == 0:
            channelID = ctx.message.channel.id
        if channelID not in ChannelIDS:
            ChannelIDS.append(channelID)
            await ctx.send("I have added the channel to the list of shop channels!")
        else:
            await ctx.send("That channel is already in the list of shop channels!")

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
    await bot.add_cog(ShopReplierCog(bot=bot))
