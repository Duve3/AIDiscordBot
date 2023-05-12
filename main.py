import discord
from discord.ext import commands
from colors import ColorsClass
from log import log, level
import os
import json

color = ColorsClass()

cogPath = "cogs."
cogList = []
for file in os.listdir(cogPath.replace(".", "/")):
    if file.endswith(".py") and not file.startswith("DISABLED_"):
        cogList.append(file.split(".")[0])


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        try:
            with open("description.txt") as descFile:
                description = descFile.read()
        except FileNotFoundError:
            description = "Placeholder description because im dumb."
            log("discord.Client.__init__()", "Description failed to load, defaulting to placeholder", level.WARNING)

        super().__init__(
            command_prefix="$",
            intents=intents,
            description=description
        )

    # the method to override in order to run whatever you need before your bot starts
    async def setup_hook(self):
        # to avoid cog getting in this list, end it with something other than .py or make it start with "DISABLED_"
        for cog in cogList:
            await self.load_extension(f"{cogPath}{cog}")


client = Client()


# makes life easier when changing cogs etc.
@client.command(name="reloadCogs")
async def reloadCogs(ctx):
    if ctx.author.id == 680116696819957810:
        log("discord.Client.Cogs.Reload", "Reloading all cogs!", level.INFO)
        for cog in cogList:
            await client.unload_extension(f"{cogPath}{cog}")
            await client.load_extension(f"{cogPath}{cog}")
        await ctx.channel.send("Reloaded all Cogs!")
    else:
        await ctx.channel.send(f"{ctx.author.mention} :gun:")


@client.event
async def on_ready():
    tabs = "\t\t\t\t\t\t\t\t\t\t\t\t\t"  # tab a bunch in order to make inline with the logging system
    log("discord.Client.ready", f"I have successfully logged in as:\n{tabs}{client.user.name}#{client.user.discriminator}\n{tabs}ID: {client.user.id}")


def main():
    try:
        with open("token.secret") as tf:
            TOKEN = tf.read()
    except FileNotFoundError:
        log("getToken", "Failed to find token inside of token.secret! Exiting...", level.ERROR)
        return
    client.run(TOKEN)


if __name__ == "__main__":
    main()
