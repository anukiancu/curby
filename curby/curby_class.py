import random
from discord.ext import commands, tasks
from discord import File
from curby.image_fetcher import get_random_kirby_pic


class Curby(commands.Cog):
    def __init__(self, bot) -> None:

        self.bot = bot
        self.ctx = None

        self.GENERAL_CHANNEL_ID = 847196702472798250

    @commands.command(help="Greets you!")
    async def hello(self, ctx):
        await ctx.send("Am Curby!")

    @commands.command(help="I say my colour.")
    async def colour(self, ctx):
        await ctx.send("Am pink!")

    @commands.command(help="I tell you my mood.")
    async def mood(self, ctx):

        moods = {
            "happ": "happ01,jpg",
            "angy": ["angy01.jpg", "angy02.jpg", "angy03.jpg"],
            "ball": "ball.jpg",
            "bonk": "bonk.jpg",
            "curb": "curb.jpg",
            "cursed": "cursed.jpg",
            "hot": "hot.jpg",
            "hungy": ["hungy01.jpg", "hungy02.jpg", "hungy03.jpg"],
            "sad": "sad.jpg",
        }

        mood, filename = random.choice(list(moods.items()))
        if type(filename) == list:
            filename = random.choice(filename)

        with open(f"moods/{filename}", "rb") as fp:
            discord_file = File(fp, filename="kirby pic.jpg")

        await ctx.send(file=discord_file, content=f"Am {mood}")

    @commands.command(help="I send a cute picture of myself.")
    async def picture(self, ctx):
        await ctx.send(
            f"""
    Henlo!
    {get_random_kirby_pic()}
        """
        )

    @tasks.loop(hours=4)
    async def daily_pic(self):
        # Our general chat
        await self.bot.wait_until_ready()
        channel_to_message = self.bot.get_channel(self.GENERAL_CHANNEL_ID)
        await channel_to_message.send(
            f"""
    @everyone Here's your daily picture of me! :3
    {get_random_kirby_pic()}
        """
        )
