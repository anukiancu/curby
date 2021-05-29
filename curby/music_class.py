import asyncio
import discord
from discord.errors import ClientException
from discord.ext.commands.errors import CommandError
from curby.music_fetcher import YTDLSource
from discord.ext import commands
import config


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.MUSIC_QUEUE = []
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

    @commands.command(help="I join a voice channel.")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(
                f"{ctx.message.author.voice} is not connected to a voice channel."
            )
            return
        else:
            voice_channel = ctx.message.author.voice.channel
        await voice_channel.connect()

    @commands.command(help="I leave the voice channel.")
    async def leave(self, ctx):
        vc = ctx.message.guild.voice_client
        if vc.is_connected():
            await vc.disconnect()
        else:
            await ctx.send("I'm not connected to any voice channels.")

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

    @commands.command(help="Select a game for me to play music from.")
    async def play_game_music(self, ctx):
        star_allies_emoji = "⭐"
        dreamland_emoji = "😴"
        message = await ctx.send("Pick a game:")
        await message.add_reaction(star_allies_emoji)
        await message.add_reaction(dreamland_emoji)

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in [
                star_allies_emoji,
                dreamland_emoji,
            ]

        reaction, user = await self.bot.wait_for("reaction_add", check=check)
        if reaction.emoji == star_allies_emoji:
            self.MUSIC_QUEUE = list(self.STAR_ALLIES_TUNES.values())

        if reaction.emoji == dreamland_emoji:
            self.MUSIC_QUEUE = list(self.DREAMLAND_TUNES.values())

        await self.play_music(ctx)

    def after(self, error):
        fut = asyncio.run_coroutine_threadsafe(
            self.play_music(self.ctx),
            self.bot.loop,
        )
        try:
            fut.result()
        except:
            # an error happened sending the message
            pass

    @commands.command(help="I play music from my games.")
    async def play_music(self, ctx):

        """try:
        song_url = tunes[tune]
        except KeyError:
            await ctx.send("Sorry, I don't know that song.")
            return"""

        try:
            server = ctx.message.guild
            voice_channel = server.voice_client
            song_url = self.MUSIC_QUEUE[0]
            self.MUSIC_QUEUE.pop(0)

            async with ctx.typing():
                filename = await YTDLSource.from_url(song_url, loop=self.bot.loop)
                try:
                    self.ctx = ctx
                    voice_channel.play(
                        discord.FFmpegPCMAudio(
                            executable=config.FFMPEG_EXECUTABLE, source=filename
                        ),
                        after=self.after,
                    )
                except ClientException:
                    await ctx.send("Please wait for the song to finish.")
                    return

            await ctx.send(f"I'm now playing {song_url}")
        except CommandError:
            await ctx.send("I'm not connected to any voice channels.")

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

    @commands.command(help="I stop playing music.")
    async def stop(self, ctx):
        vc = ctx.message.guild.voice_client
        if vc.is_playing():
            vc.stop()
            await self.leave(self, ctx)
        else:
            await ctx.send(
                "I'm not playing any music at the moment. Please use the play command."
            )
