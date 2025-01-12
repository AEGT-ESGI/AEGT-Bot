import nextcord as nc
from nextcord.ext import commands


class OnReadyEvent(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(self.bot.user, "is ready.")


def setup(bot):
    bot.add_cog(OnReadyEvent(bot))

