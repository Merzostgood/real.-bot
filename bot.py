import discord,time
from discord.ext import commands


# idk

PREFIX = '.'
intents = discord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.command()
async def spam(ctx, *, arg):
    while True:
        await arg.send("Тест")

bot.run("Here token")
