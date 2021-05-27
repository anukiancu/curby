from curby.bot import bot, daily_pic

from config import DISCORD_BOT_TOKEN

if __name__ == "__main__":
    daily_pic.start()
    bot.run(DISCORD_BOT_TOKEN)
