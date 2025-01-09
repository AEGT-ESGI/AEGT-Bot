import json
import os

import nextcord as nc
from dotenv import load_dotenv
from nextcord.ext import commands

import config


class Bot:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.getenv("TOKEN")

        self.update_config()

        self.bot = commands.Bot(intents=nc.Intents.all())

        self.cogs = []

    def update_config(self):
        config_instance = config.Config()
        self.config = config_instance.get_config()

    def load_commands(self):
        for command in os.listdir("cogs/commands"):
            if command.endswith(".py"):
                self.cogs.append("cogs.commands." + command[:-3])

    def load_events(self):
        for event in os.listdir("cogs/events"):
            if event.endswith(".py"):
                self.cogs.append("cogs.events." + event[:-3])

    def load(self):
        self.load_events()
        self.load_commands()
        self.bot.load_extensions(self.cogs)

    def run(self):
        self.bot.run(self.bot_token)


if __name__ == "__main__":
    bot = Bot()
    bot.load()
    bot.run()
