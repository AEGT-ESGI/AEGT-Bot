import json
import os

import nextcord as nc
from dotenv import load_dotenv
from nextcord.ext import commands


class Bot:
    def __init__(self, config_file_path: str = "config.json"):
        load_dotenv()

        self.update_config()

        self.bot = commands.Bot(intents=nc.Intents.all())

        self.cogs = []

    def update_config(self):
        if not os.path.exists("config.json"):
            raise FileNotFoundError("Configuration file not found.")
        with open("config.json", encoding="utf-8") as config_file:
            self.config = json.load(config_file)

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
        self.bot.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    bot = Bot()
    bot.load()
    bot.run()
