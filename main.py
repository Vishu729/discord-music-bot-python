import discord
from discord.ext import commands
import music

cogs = [music]


client = commands.Bot (command_prefix='!', intents = discord.Intents.all())


for i in range(len(cogs)):
        cogs[i].setup(client)



client.run("OTg2NTQ2NjkwMDc5MjIzODM4.GoH7oZ.t7lkIcHoHEjANMKIloKBE91c-NC2zZI-1c8DCc")