import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=">")


@bot.command()
async def hello(ctx):
    await ctx.send("Am Curby!")


@bot.command()
async def colour(ctx):
    await ctx.send("Am pink!")


@bot.command()
async def poyo(ctx):
    await ctx.send("Poyo! :3")
