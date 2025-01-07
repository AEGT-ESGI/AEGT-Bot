import nextcord as nc
from nextcord.ext import commands
from os import listdir, getenv
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(intents=nc.Intents.all())

@bot.event
async def on_ready():
    print("Bot is connected.")

cogs = []

for C in listdir("cogs/commands"):
    if C.endswith(".py"):
        cogs.append("cogs.commands."+C[:-3])

for C in listdir("cogs/events"):
    if C.endswith(".py"):
        cogs.append("cogs.events."+C[:-3])

bot.load_extensions(cogs)

bot.run(getenv("TOKEN"))
