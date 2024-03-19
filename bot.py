import discord,time
from discord.ext import commands


# idk

TOKEN = 'MTE5ODk1ODA2MzIwNjUzOTI4NQ.G4DuUi.U9usc0-KG-p8R1roQ5GWR9ibWymqLl84DRWpu4'
PREFIX = '.'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.command()
async def spam(ctx, *, arg):
    while True:
        await arg.send("Тест")

bot.run("MTE5ODk1ODA2MzIwNjUzOTI4NQ.G4DuUi.U9usc0-KG-p8R1roQ5GWR9ibWymqLl84DRWpu4")
