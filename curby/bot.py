from discord.ext.commands.errors import CommandError
from curby.music_fetcher import YTDLSource
import random
from pathlib import Path
import discord
import config
from discord import voice_client
from discord.ext import commands, tasks
from discord import File
from curby.image_fetcher import get_random_kirby_pic


GENERAL_CHANNEL_ID = 847196702472798250


tunes = {
    "dreamland_file_select": "https://www.youtube.com/watch?v=vjWydqMtt5U",
    "dreamland_title_theme": "https://www.youtube.com/watch?v=r9MOP411n_o",
}
pictures = list(Path("memes").glob("**/*"))
sanitized_pictures = [str(pic) for pic in pictures]
# intents = discord.Intents().all()
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


@bot.command(help="I join a voice channel.")
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(
            f"{ctx.message.author.voice} is not connected to a voice channel."
        )
        return
    else:
        voice_channel = ctx.message.author.voice.channel
    await voice_channel.connect()


@bot.command(help="I leave the voice channel.")
async def leave(ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_connected():
        await vc.disconnect()
    else:
        await ctx.send("I'm not connected to any voice channels.")


@bot.command(help="I play music from my games.")
async def play(ctx, tune):
    if tune == "help":
        await ctx.send(f"Here's a list of songs I can play: {', '.join(tunes.keys())}")
        return

    try:
        song_url = tunes[tune]
    except KeyError:
        await ctx.send("Sorry, I don't know that song.")
        return

    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        filename = await YTDLSource.from_url(song_url, loop=bot.loop)
        voice_channel.play(
            discord.FFmpegPCMAudio(executable=config.FFMPEG_EXECUTABLE, source=filename)
        )
        await ctx.send(f"I'm now playing {tune}")
    except CommandError:
        await ctx.send("I'm not connected to any voice channels.")


@tasks.loop(hours=4)
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
