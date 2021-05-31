import discord
from discord.ext import commands
from curby.curby_class import Curby
from curby.music_class import Music

from config import DISCORD_BOT_TOKEN


intents = discord.Intents().default()
bot = commands.Bot(command_prefix=">")

music = Music(bot)
curby_instance = Curby(bot)

bot.add_cog(music)
bot.add_cog(curby_instance)

bot.remove_command("play_music")

if __name__ == "__main__":
    curby_instance.daily_pic.start()
    bot.run(DISCORD_BOT_TOKEN)
