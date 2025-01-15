import nextcord as nc
from nextcord.ext import commands
from config import TicketConfig

tc = TicketConfig()


class TicketEventUtils:
    @staticmethod
    def generate_ticket_id(user_id: int) -> int:
        return sum([int(i) for i in str(user_id)])

    @staticmethod
    async def create_ticket_channel(
            interaction: nc.Interaction,
            category: nc.CategoryChannel,
            role: nc.Role,
            ticket_id: int
            ) -> nc.TextChannel:
        return await category.create_text_channel(
                name=f"ticket-{ticket_id}",
                topic=str(interaction.user.id),
                overwrites={
                    interaction.guild.default_role: nc.PermissionOverwrite(read_messages=False),
                    role: nc.PermissionOverwrite(read_messages=True)
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
            if interaction.data["custom_id"].startswith("create_ticket"):

                category_id, role_id = interaction.data["custom_id"].split("-")[1:]

                await self.handle_ticket_creation(interaction, category_id, role_id)

    async def handle_ticket_creation(self, interaction: nc.Interaction, category_id: int, role_id: int):
        category: nc.CategoryChannel = await interaction.guild.fetch_channel(category_id)
        role: nc.Role = await interaction.guild.fetch_role(role_id)

        ticket_id = TicketEventUtils.generate_ticket_id(interaction.user.id)

        channel = await TicketEventUtils.create_ticket_channel(interaction, category, role, ticket_id)
        embed = TicketEventUtils.create_welcome_embed()

        await interaction.send("Ta carte étudiante est en cours de vérification, tu recevras tes accès si elle est valide.", ephemeral=True)
        await channel.send(embed=embed)
        await TicketEventUtils.send_and_delete_mention(
                channel,
                interaction.user.id,
                tc.get_ticket_role()
                )


def setup(bot):
    bot.add_cog(ManageTicketEvent(bot))

