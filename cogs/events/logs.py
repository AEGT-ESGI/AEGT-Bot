import nextcord as nc
from nextcord.ext import commands
from config import LogConfig

lc = LogConfig()


class LogsSystem(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.actions = {
            1: "guild_update",
            10: "channel_create",
            11: "channel_update",
            12: "channel_delete",
            20: "kick",
            22: "ban",
            23: "unban",
            24: "member_update",
            25: "member_role_update",
            30: "role_create",
            31: "role_update",
            32: "role_delete",
            60: "emoji_create",
            62: "emoji_delete",
            72 :"message_delete"
            }
        
    @commands.Cog.listener()
    async def on_guild_audit_log_entry_create(self, entry: nc.AuditLogEntry):
        channel, title = await self.get_channel_if_admissible(entry)

        if not channel:
            return
        
        await self.send_embed(
            title=title,
            fields={
                'Target': entry.target,
                'Reason': entry.reason,
                'Extra': entry.extra
            },
            channel=channel
        )

    async def get_channel_if_admissible(self, entry: nc.AuditLogEntry) -> tuple[nc.TextChannel, str] | tuple[None, None]:

        if not entry.action in self.actions.keys():
            return None, None
        
        text_action = self.actions[entry.action]

        if not text_action in lc.get_logs_active():
            return None, None
        
        channel = await entry.guild.fetch_channel(lc.get_logs_channel())

        if not channel:
            return None, None
        
        return channel, text_action.replace('_', ' ').title()

    async def send_embed(self, title: str, fields: dict, channel: nc.TextChannel):
        embed = nc.Embed(
            title=title
        )
        for name, value in fields.items():
            embed.add_field(name=name, value=value)
        
        await channel.send(embed=embed)
    

def setup(bot):
    bot.add_cog(LogsSystem(bot))

