# Curby

Curby is a cute little Discord bot for all your Kirby needs!

```
Curby:
  hello           Greets you!
  colour          I say my colour.
  decide          Ask me someting, and I'll give you advice.
  mood            I tell you my mood.
  pick            I help you pick between things (separated by a comma)
  picture         I send a cute picture of myself.
Music:
  leave           I leave the voice channel.
  pause           I pause the music.
  play_game_music Select a game for me to play music from.
  previous        I play the previous song in the queue.
  queue           Display the current queue.
  resume          I resume playing music.
  shuffle         I shuffle through songs.
  skip            I play the next song in the queue.
  songs           A list of tunes I can play.
```

It also sends cute pictures of Kirby every 4 hours.

# Dependencies
- Python 3.7 and above
- FFmpeg
- A Discord app

# Creating the Discord app
Navigate to [Discord's Developer Portal](https://discord.com/developers/applications).

- Select "New Application" in the top left corner
- Choose a name for your application
- Select "Bot", create the bot and click the "copy token" button - save this token somewhere handy.

## Inviting the bot to your server
- Select "OAuth2" from the sidebar
- Scroll down until you find `Scopes`
- Select `Bot` and copy the url displayed in the textbox below

You can invite the bot to any server you have "Manage Server" permissions on.


# FFMPEG

You can download FFMPEG from [their homepage](http://ffmpeg.org/download.html).

You can usually find the executable for the Windows builds located in the `bin` folder of the downloaded zip file.


# Installation

- Clone the repository
- Use your favorite package manager to install Curby's dependencies

Using something like `poetry`, you would run `poetry install`, in Curby's root directory.

# Setup

Create an empty `config.py` file in Curby's root directory and set it up like so:

```
DISCORD_BOT_TOKEN = "your_token_here"
FFMPEG_EXECUTABLE = "your_ffmpeg_executable_path"
```

Store the token you copied from the Discord Developer Portal in the `DISCORD_BOT_TOKEN` variable.
Set the path for your FFMPEG executable in `FFMPEG_EXECUTABLE`.

**Windows users**: Python expects that paths that use a backslash as a separator has a second backslash in the folder name. 

*Example*: `C:\ffmpeg\ffmpeg.exe` should be referenced as `C:\\ffmpeg\\ffmpeg.exe`.

# Running Curby

To run the bot, simply execute `python -m curby` while in Curby's virtual environment.

*Hint: If using `poetry`, you can do this with `poetry shell`.*

This however means that Curby will stop when the Python instance is killed. *Consider using a task scheduler on Windows or a terminal multiplexer on Linux or macOS to keep Curby alive.*