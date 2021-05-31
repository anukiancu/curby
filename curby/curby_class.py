import random
import discord
from discord.ext import commands, tasks
from discord import File, file
from curby.image_fetcher import get_random_kirby_pic


class Curby(commands.Cog):
    def __init__(self, bot) -> None:

        self.bot = bot
        self.ctx = None

        self.GENERAL_CHANNEL_ID = 847196702472798250

    @commands.command(help="Greets you!")
    async def hello(self, ctx):
        await ctx.send(
            "Am Curby! https://gfycat.com/dearesthideousamethystgemclam-nintendo-kirby"
        )

    @commands.command(help="I say my colour.")
    async def colour(self, ctx):
        await ctx.send("Am pink!")

    @commands.command(help="I help you pick between things (separated by a comma).")
    async def pick(self, ctx, *message):
        message_string = " ".join(message)
        message_list = message_string.split(",")
        random_pick = random.choice(message_list)
        await ctx.send(random_pick)

    @commands.command(help="I tell you my mood.")
    async def mood(self, ctx):

        moods = {
            "happ": "happ01.jpg",
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

    @commands.command(help="I do a cute dance!")
    async def dance(self, ctx):
        await ctx.send("https://imgur.com/LqFVtHA")

    @commands.command(help="Ask me someting, and I'll give you advice.")
    async def decide(self, ctx, *args):
        decisions = ["Yes!", "Hmm, no.", "Maybe?", "Ask again later."]
        random_decision = random.choice(decisions)
        await ctx.send(random_decision)

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
        for guild in self.bot.guilds:
            channel_to_message = guild.text_channels[0]
            await channel_to_message.send(
                f"""
Here's your daily picture of me! :3
{get_random_kirby_pic()}
            """
            )
