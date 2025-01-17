import nextcord as nc
from nextcord.ext import commands
from config import TicketConfig
from nextcord.ui import Modal

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
    def create_verification_embed(user: nc.User) -> nc.Embed:
        embed = nc.Embed(
                title=f"Vérification de {user}",
                description="En attente de la carte étudiante...",
                color=nc.Color.green()
                )
        return embed

    @staticmethod
    async def send_and_delete_mention(channel: nc.TextChannel, staff_role_id: int):
        msg = await channel.send(f"<@&{staff_role_id}>")
        await msg.delete()


class ManageTicketEvent(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self, interaction: nc.Interaction):
        if interaction.type == nc.InteractionType.component:
            if interaction.data["custom_id"].startswith("create_ticket"):

                category_id, role_id = interaction.data["custom_id"].split("-")[1:]

                await self.ask_for_student_card(interaction, interaction.user)
                await self.handle_ticket_creation(interaction, category_id, role_id)

    async def ask_for_student_card(self, interaction: nc.Interaction, user: nc.User):
        pass
    
    async def handle_ticket_creation(self, interaction: nc.Interaction, category_id: int, role_id: int):
        category: nc.CategoryChannel = await interaction.guild.fetch_channel(category_id)
        role: nc.Role = await interaction.guild.fetch_role(role_id)

        ticket_id = TicketEventUtils.generate_ticket_id(interaction.user.id)

        channel = await TicketEventUtils.create_ticket_channel(interaction, category, role, ticket_id)
        embed = TicketEventUtils.create_verification_embed(interaction.user)

        await channel.send(embed=embed)
        await TicketEventUtils.send_and_delete_mention(
                channel,
                role_id
                )

def setup(bot):
    bot.add_cog(ManageTicketEvent(bot))

