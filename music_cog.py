import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #status of the music bot
        self.is_playing = False
        self.is_paused = False

        # checking the song thats playing and its quality using a 2d array
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

     #search for music on yt
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}
def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # infinite loop checking 
async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
            
            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

@commands.command(name="play", aliases=["p","playing"], help="Plays a selected song from youtube")
async def play(self, ctx, *args):
        query = " ".join(args)
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            #you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music(ctx)

@commands.command(name="pause", help="Pauses the current song being played")
async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()

@commands.command(name = "resume", aliases=["r"], help="Resumes playing with the discord bot")
async def resume(self, ctx, *args):
        if self.is_paused:
            self.vc.resume()

@commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)


@commands.command(name="queue", aliases=["q"], help="Displays the current songs in queue")
async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            # display a max of 5 songs in the current queue
            if (i > 4): break
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

@commands.command(name="clear", aliases=["c", "bin"], help="Stops the music and clears the queue")
async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")

@commands.command(name="leave", aliases=["disconnect", "l", "d"], help="Kick the bot from VC")
async def dc(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

''' class music(commands.Cog):
       def __init__(self, client):
             self.client = client

@commands.command(name= 'Join')
async def join(self,ctx):
        if ctx.author.voice is None:
                await ctx.send("You're not in a voice channel!")
                voice_channel = ctx.author.voice.channel 
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

@commands.command(name="Play")
async def play(self,ctx,url):
     ctx.voice_client.stop()
     FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
     YDL_OPTIONS = {'format' : "bestaudio"}
     vc=ctx.voice_client

     with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
         info=ydl.extract_info(url, download=False)
         url2 = info['formats'][0]['url']
         source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
         vc.play(source)

@commands.command(name="pause")
async def pause(self,ctx):
     await ctx.voice_client.pause()
     await ctx.send("Paused!")

@commands.command(name="resume")
async def resume(self,ctx):
     await ctx.voice_client.resume()
     await ctx.send("Resume")

@commands.command(name="disconnect")
async def disconnected(self,ctx):
     await ctx.voice_client.disconnect()

def setup(client):
        client.add_cog(music(client))
'''
