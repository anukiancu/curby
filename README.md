# Curby
Clone the project and run `poetry install` and then `poetry shell` 

To set it up, first go to [Discord Developer Portal](https://discord.com/developers/applications), click "new application", go to the bot and click the "copy token" button. After that, create an empty config.py file and set it up like so:

```
DISCORD_BOT_TOKEN = "your_token_here"
FFMPEG_EXECUTABLE = "your_fmmpeg_executable_path"
```
If you don't have FFmpeg, download it and copy the path to the executable in your config file. You can then run the bot with the following command:

```
python -m curby
```