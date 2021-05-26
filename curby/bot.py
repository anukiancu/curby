import discord
import random
from pathlib import Path
from discord.ext import commands
from discord import File


pictures = list(Path("Pics").glob("**/*"))
sanitized_pictures = [str(pic) for pic in pictures]
bot = commands.Bot(command_prefix=">")


@bot.command()
async def hello(ctx):
    await ctx.send("Am Curby!")


@bot.command()
async def colour(ctx):
    await ctx.send("Am pink!")


@bot.command()
async def poyo(ctx):

    todays_picture = random.choice(sanitized_pictures)

    with open(todays_picture, "rb") as fp:
        discord_file = File(fp, filename="kirby pic.jpg")

    await ctx.send(file=discord_file)


@bot.command()
async def commands(ctx):
    command_help = """
    ```
Hi. Am Curby. Here's a list of commands:
>hello: Greets you.
>colour: I say my colour.
>poyo: Sends a random picture of me.
```
"""
    await ctx.send(command_help)
