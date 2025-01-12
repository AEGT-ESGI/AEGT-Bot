import nextcord as nc
from nextcord.ext import commands
from config import TicketConfig as tc


class TicketEventUtils:
    @staticmethod
    def generate_ticket_id(user_id: int) -> int:
        return sum([int(i) for i in str(user_id)])

    @staticmethod
    async def create_ticket_channel(
            interaction: nc.Interaction,
            category: nc.CategoryChannel,
            ticket_id: int
            ) -> nc.TextChannel:
        return await category.create_text_channel(
                name=f"ticket-{ticket_id}",
                topic=str(interaction.user.id),
                overwrites={
                    interaction.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                    interaction.guild.get_role(get_value("STAFF_ROLE_ID")): nc.PermissionOverwrite(read_messages=True),
                    interaction.user: nc.PermissionOverwrite(read_messages=True)
                    }
                )

    @staticmethod
    def create_welcome_embed() -> nc.Embed:
        return nc.Embed(
                title="Bienvenue à 𝐿'𝛼𝜋𝜏𝜄𝑞𝜇𝜀 ! ☕",
                description=(
                    "Merci de répondre aux questions suivantes afin de valider ton arrivée sur le serveur! "
                    "Un membre du staff te répondra dès que possible. 🐸\n\n"
                    "🍉 Quel âge as-tu ?\n"
                    "🍉 Que cherches-tu sur ce serveur?"
                    ),
                color=nc.Color.green()
                )

    @staticmethod
    async def send_and_delete_mention(channel: nc.TextChannel, user_id: int, staff_role_id: int):
        msg = await channel.send(f"<@{user_id}><@&{staff_role_id}>")
        await msg.delete()


class ManageTicketEvent(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nc.Interaction):
        if interaction.type == nc.InteractionType.component:
            if interaction.data["custom_id"] == "create_ticket":
                await self.handle_ticket_creation(interaction)

    async def handle_ticket_creation(self, interaction: nc.Interaction):
        category: nc.CategoryChannel = await interaction.guild.fetch_channel(tc.get_ticket_channel())
        ticket_id = TicketEventUtils.generate_ticket_id(interaction.user.id)

        channel = await TicketEventUtils.create_ticket_channel(interaction, category, ticket_id)
        embed = TicketEventUtils.create_welcome_embed()

        await interaction.send("Le ticket a été créé ! <:yay:1274376322847739935>", ephemeral=True)
        await channel.send(embed=embed)
        await TicketEventUtils.send_and_delete_mention(
                channel,
                interaction.user.id,
                tc.get_ticket_role()
                )


def setup(bot):
    bot.add_cog(ManageTicketEvent(bot))

