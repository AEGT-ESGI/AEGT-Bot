import nextcord as nc
from nextcord.ext import commands
from config import BotConfig

bt = BotConfig()


class OnReadyEvent(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot_version = bt.get_bot_version()

    @commands.Cog.listener()
    async def on_ready(self):
        bt.set_bot_name(self.bot.user.name)

        activity = nc.Activity(
            type=nc.ActivityType.custom,
            name="Version",
            state=self.bot_version,
            )

        await self.bot.change_presence(activity=activity)
        print(self.bot.user, "is ready!")


def setup(bot):
    bot.add_cog(OnReadyEvent(bot))

