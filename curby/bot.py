import random
from pathlib import Path
import discord
from discord.ext import commands, tasks
from discord import File
from curby.image_fetcher import get_random_kirby_pic


GENERAL_CHANNEL_ID = 847196702472798250

pictures = list(Path("memes").glob("**/*"))
sanitized_pictures = [str(pic) for pic in pictures]
bot = commands.Bot(command_prefix=">")


@bot.command(help="Greets you!")
async def hello(ctx):
    await ctx.send("Am Curby!")


@bot.command(help="I say my colour.")
async def colour(ctx):
    await ctx.send("Am pink!")


@bot.command(help="Sends a random meme of me.")
async def poyo(ctx):

    todays_picture = random.choice(sanitized_pictures)

    with open(todays_picture, "rb") as fp:
        discord_file = File(fp, filename="kirby pic.jpg")

    await ctx.send(file=discord_file)


@tasks.loop(seconds=5)
async def daily_pic():
    # Our general chat
    await bot.wait_until_ready()
    channel_to_message = bot.get_channel(GENERAL_CHANNEL_ID)
    await channel_to_message.send(
        f"""
    @everyone Here's your daily picture of me! :3
    {get_random_kirby_pic()}
    """
    )
