# flake8: noqa E501

import asyncio
import discord
from discord.colour import Colour
from discord.errors import ClientException
from discord.ext.commands.errors import CommandError
from curby.youtube_dl_source import YTDLSource
from discord.ext import commands
import config
import random
import datetime


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_queue = []
        self.previous = False
        self.music_queue_position = -1
        self.server_queue = {}
        self.DREAMLAND_TUNES = {
            "dreamland_file_select": "https://www.youtube.com/watch?v=vjWydqMtt5U",
            "dreamland_title_theme": "https://www.youtube.com/watch?v=r9MOP411n_o",
            "dreamland_visitor": "https://www.youtube.com/watch?v=k2CtoaatCOA",
            "dreamland_lor_starcutter": "https://www.youtube.com/watch?v=tW_oW-KbV8I",
            "dreamland_pop_star": "https://www.youtube.com/watch?v=XDo4F-igrJ0",
            "dreamland_adventure": "https://www.youtube.com/watch?v=vZBStYy7oSg",
            "dreamland_looming_darkness": "https://www.youtube.com/watch?v=4sdBPRliIkM",
            "dreamland_dance": "https://www.youtube.com/watch?v=Duy7jw4be_U",
            "dreamland_onion_ocean": "https://www.youtube.com/watch?v=W86kUYu18Ag",
            "dreamland_happy_mambo": "https://www.youtube.com/watch?v=L5eU-DP3o6M",
            "dreamland_aqua_area": "https://www.youtube.com/watch?v=YnrsTiru2QU",
            "dreamland_rainy_area": "https://www.youtube.com/watch?v=9kMmBaO4Id8",
            "dreamland_white_wafers": "https://www.youtube.com/watch?v=7Q4iA-USvBo",
            "dreamland_key_challenge": "https://www.youtube.com/watch?v=SRqtS-YK7dU",
            "dreamland_sky_walz": "https://www.youtube.com/watch?v=Dz5xqZUmW2Q",
            "dreamland_final_battle": "https://www.youtube.com/watch?v=2hetvwkxC9Q",
            "dreamland_theme": "https://www.youtube.com/watch?v=rb6MMKV6dPY",
            "dreamland_training": "https://www.youtube.com/watch?v=uJKgwffy75",
            "dreamland_candy_chaos": "https://www.youtube.com/watch?v=Lo56B3YqGUw",
        }
        self.STAR_ALLIES_TUNES = {
            "star_allies_friends": "https://www.youtube.com/watch?v=gbquTu-1eXU",
            "star_allies_title_screen": "https://www.youtube.com/watch?v=YS16xTk5RSc",
            "star_allies_green_gardens": "https://www.youtube.com/watch?v=2nzoXVP0g4o",
            "star_allies_gallery": "https://www.youtube.com/watch?v=rzitiHvyZ7I",
            "star_allies_friendly_field": "https://www.youtube.com/watch?v=oYIJF1nbgTk",
            "star_allies_gatehouse_road": "https://www.youtube.com/watch?v=8HhbMA5HTvY",
            "star_allies_earthfall": "https://www.youtube.com/watch?v=wUuvwY8wr68",
            "star_allies_misteen": "https://www.youtube.com/watch?v=3RSf5PkrfzA",
            "star_allies_caverna": "https://www.youtube.com/watch?v=MHjtISmDg1o",
            "star_allies_frostak": "https://www.youtube.com/watch?v=5IDgoF8Wixg",
            "star_allies_towara": "https://www.youtube.com/watch?v=80cNiB-rMuc",
            "star_allies_final_push": "https://www.youtube.com/watch?v=66rO9DfSOZs",
            "star_allies_curtain_call": "https://www.youtube.com/watch?v=hlixHVj3BtM",
            "star_allies_ability_room": "https://www.youtube.com/watch?v=H6aVLi31LGw",
            "star_allies_patched_plains": "https://www.youtube.com/watch?v=hH0pfE56kcg",
            "star_allies_staff_roll3": "https://www.youtube.com/watch?v=Cluxc2kYbhU",
            "star_allies_squeaks_remix": "https://www.youtube.com/watch?v=zs2Y6mVZljQ",
            "star_allies_shadowy_partners": "https://www.youtube.com/watch?v=Dk1dR0M65ak",
            "star_allies_adventure_begins": "https://www.youtube.com/watch?v=qk4zTsprobs",
            "star_allies_curtain_call02": "https://www.youtube.com/watch?v=OCbmL70SIXg",
            "star_allies_shape_of_a_heart": "https://www.youtube.com/watch?v=G59SZ0hpo5I",
            "star_allies_let_them_know_were_happy": "https://www.youtube.com/watch?v=6R7s0TANojM",
        }

    async def generate_embed(self, url, position=None):
        data = await YTDLSource.fetch_info(url, loop=self.bot.loop)
        embed = discord.Embed(
            url=data.get("webpage_url"),
            title=data.get("title"),
            description=f"Duration • {datetime.timedelta(seconds=data.get('duration'))}",  # noqa: E501
        )
        embed.set_image(url=data.get("thumbnail"))
        embed.set_author(name=data.get("uploader"))

        if position:
            embed.set_footer(text=f"Position in queue: {position}")
        embed.color = Colour.magenta()
        return embed

    @commands.command(help="A list of tunes I can play.")
    async def songs(self, ctx):
        nl = "\n"
        dreamland_songs = f"""
    ```RETRUN TO DREAMLAND:
        {nl}{nl.join(self.DREAMLAND_TUNES.keys())}
        ```
        """
        star_allies_songs = f"""
    ```STAR ALLIES:
        {nl}{nl.join(self.STAR_ALLIES_TUNES.keys())}
        ```
        """
        await ctx.send(dreamland_songs)
        await ctx.send(star_allies_songs)

    @commands.command(help="Display the current queue.")
    async def queue(self, ctx):
        if not self.server_queue[ctx.message.guild.id]["music_queue"]:
            await ctx.send("The queue is empty!")
            return

        arrow_left = "⬅️"
        arrow_right = "➡️"
        arrow_up = "⤴"

        await ctx.send(
            f"""
Use {arrow_left} to go backwards, and {arrow_right} to go forwards in the queue.
You can play the highlighted song next clicking {arrow_up}!'
        """
        )

        # iterator = self.music_queue_position
        iterator = self.server_queue[ctx.message.guild.id]["music_queue_position"]
        message = await ctx.send(
            embed=await self.generate_embed(
                self.music_queue[iterator], position=iterator + 1
            )
        )

        await message.add_reaction(arrow_left)
        await message.add_reaction(arrow_right)
        await message.add_reaction(arrow_up)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in [
                arrow_left,
                arrow_right,
                arrow_up,
            ]

        while True:
            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=30
                )
                if reaction.emoji == arrow_left:
                    iterator -= 1
                    await message.edit(
                        embed=await self.generate_embed(
                            self.server_queue[ctx.message.guild.id]["music_queue"][
                                iterator
                            ],
                            position=iterator + 1,
                        )
                    )
                    await message.remove_reaction(reaction, user)

                if reaction.emoji == arrow_up:
                    embed = await self.generate_embed(
                        self.server_queue[ctx.message.guild.id]["music_queue"][
                            iterator
                        ],
                        position=iterator,
                    )

                    # Skew position to count from 1 instead of -1
                    embed.set_footer(
                        text=f"The song has been moved to position {self.server_queue[ctx.message.guild.id]['music_queue_position'] + 2}"  # noqa: E501
                    )

                    self.server_queue[ctx.message.guild.id]["music_queue"].insert(
                        self.server_queue[ctx.message.guild.id]["music_queue_position"]
                        + 1,
                        self.server_queue[ctx.message.guild.id]["music_queue"].pop(
                            iterator
                        ),
                    )

                    await message.edit(embed=embed)
                    await message.remove_reaction(reaction, user)

                if reaction.emoji == arrow_right:
                    iterator += 1
                    await message.edit(
                        embed=await self.generate_embed(
                            self.server_queue[ctx.message.guild.id]["music_queue"][
                                iterator
                            ],
                            position=iterator + 1,
                        )
                    )
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                break

    """@commands.command(help="I join a voice channel.")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(f"You need to be connected to a voice channel.")
            return
        else:
            voice_channel = ctx.message.author.voice.channel
        await voice_channel.connect(reconnect=True, timeout=12000)"""

    @commands.command(help="Select a game for me to play music from.")
    async def play_game_music(self, ctx):
        # MUSIC_QUEUE_POSITION determines which element in MUSIC_QUEUE gets played.
        # It's reset in this function to prevent a bug where play_game_music uses the
        # same position from the last time it was ran.
        # self.music_queue_position = -1

        # Initialize music queue for server ID
        self.server_queue[ctx.message.guild.id] = {"music_queue_position": -1}

        star_allies_emoji = "⭐"
        dreamland_emoji = "😴"
        vc = ctx.message.guild.voice_client
        if not vc:
            if not ctx.message.author.voice:
                await ctx.send("You need to be connected to a voice channel.")
                return
            else:
                voice_channel = ctx.message.author.voice.channel

        await voice_channel.connect(reconnect=True, timeout=12000)

        message = await ctx.send(
            "Pick a game (press the star for Star Allies and sleepy for Return to Dreamland)."  # noqa: E501
        )
        await message.add_reaction(star_allies_emoji)
        await message.add_reaction(dreamland_emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in [
                star_allies_emoji,
                dreamland_emoji,
            ]

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        if reaction.emoji == star_allies_emoji:
            self.server_queue[ctx.message.guild.id]["music_queue"] = list(
                self.STAR_ALLIES_TUNES.values()
            )
            # self.music_queue = list(self.STAR_ALLIES_TUNES.values())

        if reaction.emoji == dreamland_emoji:
            self.server_queue[ctx.message.guild.id]["music_queue"] = list(
                self.DREAMLAND_TUNES.values()
            )
            self.music_queue = list(self.DREAMLAND_TUNES.values())

        await self.play_music(ctx)
        await message.delete()

    @commands.command()
    async def play_music(self, ctx):
        try:
            voice_channel = ctx.message.guild.voice_client
            if not self.previous:
                # self.music_queue_position += 1
                self.server_queue[ctx.message.guild.id]["music_queue_position"] += 1
            else:
                # self.music_queue_position -= 1
                self.server_queue[ctx.message.guild.id]["music_queue_position"] -= 1

            music_queue_position = self.server_queue[ctx.message.guild.id][
                "music_queue_position"
            ]
            song_url = self.server_queue[ctx.message.guild.id]["music_queue"][
                music_queue_position
            ]

            async with ctx.typing():
                filename = await YTDLSource.from_url(song_url, loop=self.bot.loop)
                try:
                    voice_channel.play(
                        discord.FFmpegPCMAudio(
                            executable=config.FFMPEG_EXECUTABLE, source=filename
                        ),
                        after=lambda x: asyncio.run_coroutine_threadsafe(
                            self.play_music(ctx), self.bot.loop
                        ),
                    )
                except ClientException as e:
                    await ctx.send(e)
                    return

            await ctx.send(f"I'm now playing {song_url}")
        except CommandError:
            await ctx.send("I'm not connected to any voice channels.")

        music = discord.Game("Music")
        await self.bot.change_presence(activity=music)

    @commands.command(help="I shuffle through songs.")
    async def shuffle(self, ctx):
        if self.music_queue:
            random.shuffle(self.music_queue)
            await ctx.send("I'm now shuffling through the playlist.")

    @commands.command(help="I pause the music.")
    async def pause(self, ctx):
        vc = ctx.message.guild.voice_client
        if vc.is_playing():
            vc.pause()
        else:
            await ctx.send(
                "I'm not playing any music at the moment. Please use the play command"
            )

    @commands.command(help="I resume playing music.")
    async def resume(self, ctx):
        vc = ctx.message.guild.voice_client
        if vc.is_paused():
            vc.resume()
        else:
            await ctx.send(
                "I'm not playing any music at the moment. Please use the play command."
            )

    @commands.command(help="I play the next song in the queue.")
    async def skip(self, ctx):
        self.previous = False

        vc = ctx.message.guild.voice_client

        if vc:
            if not ctx.message.author.voice:
                await ctx.send(
                    "You need to be connected to a voice channel to run skip."
                )
                return

        if vc.is_playing():
            vc.stop()
        else:
            await ctx.send(
                "I'm not playing any music at the moment. Please use the play command."
            )

    @commands.command(help="I play the previous song in the queue.")
    async def previous(self, ctx):
        self.previous = True

        vc = ctx.message.guild.voice_client
        if vc.is_playing():
            vc.stop()
        else:
            await ctx.send(
                "I'm not playing any music at the moment. Please use the play command."
            )

    @commands.command(help="I leave the voice channel.")
    async def leave(self, ctx):
        vc = ctx.message.guild.voice_client

        if vc:
            if not ctx.message.author.voice:
                await ctx.send(
                    "You need to be connected to a voice channel to run skip."
                )
                return

        if vc.is_connected():
            await vc.disconnect()
        else:
            await ctx.send("I'm not connected to any voice channels.")
        del self.server_queue[ctx.message.guild.id]
