import nextcord as nc
from nextcord.ext import commands
from nextcord.ui import Button, View
from time import sleep
from config import TicketConfig, SchoolConfig

tc = TicketConfig()
sc = SchoolConfig()


class TicketUtils:
    @staticmethod
    def user_has_permission(interaction: nc.Interaction) -> bool:
        return (
                interaction.user.top_role.permissions.manage_channels or
                interaction.user.top_role.permissions.administrator or
                interaction.user.id == interaction.guild.owner_id
                )

    @staticmethod
    async def handle_existing_ticket_system(interaction: nc.Interaction, ticket_category: nc.CategoryChannel, support_role: nc.Role):
        view = View()
        view.add_item(Button(
            style=nc.ButtonStyle.danger,
            label="Supprimer l'ancien système de tickets",
            custom_id="delete_ticket"
            ))
        view.add_item(Button(
            style=nc.ButtonStyle.primary,
            label="Annuler",
            custom_id="cancel"
            ))

        view.interaction_check = lambda i: TicketUtils.allow_ticket_creation(i, ticket_category, support_role)

        await interaction.send(
                "Il y a déjà un système de tickets, tu veux vraiment le supprimer pour en créer un nouveau ?",
                view=view
                )

    @staticmethod
    async def setup_new_ticket_system(interaction: nc.Interaction, ticket_category: nc.CategoryChannel, support_role: nc.Role):
        tc.set_ticket_category(ticket_category.id)

        await interaction.send(
                "Le système de tickets a été configuré !"
                )

        await TicketUtils.send_ticket_embed(interaction.channel, ticket_category, support_role)

        sleep(3)
        await interaction.delete_original_message()

    @staticmethod
    async def allow_ticket_creation(interaction: nc.Interaction, ticket_category: nc.CategoryChannel, support_role: nc.Role):
        if interaction.data["custom_id"] == "delete_ticket":
            tc.set_ticket_category(ticket_category.id)

            await interaction.message.edit(
                    "Le système de tickets a été configuré !",
                    view=None
                    )

            await TicketUtils.send_ticket_embed(interaction.channel, ticket_category, support_role)

            sleep(3)
            await interaction.message.delete()
        else:
            await interaction.message.edit(
                    "Configuration annulée.",
                    view=None
                    )

            sleep(3)
            await interaction.message.delete()

    @staticmethod
    async def send_ticket_embed(channel: nc.TextChannel, ticket_category: nc.CategoryChannel, support_role: nc.Role):
        view = View()
        view.add_item(Button(
            style=nc.ButtonStyle.primary,
            label="Démarrer la vérification",
            custom_id=f"create_ticket-{ticket_category.id}-{support_role.id}"
            ))

        embed = nc.Embed(
                title="Vérification du statut étudiant",
                description="Pour demander un accès au statut étudiant, veuillez cliquer sur le bouton ci-dessous.\n-# Votre carte étudiante vous sera demandée, saisissez vous en.\n-# Elle ne sera en aucun cas sauvegardée.",
                color=nc.Color.green()
                )

        await channel.send(embed=embed, view=view)


class ManageTicketCommand(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @nc.slash_command(description="Mettre en place le système de tickets.")
    async def configurer_tickets(
            self,
            interaction: nc.Interaction,
            ticket_category: nc.CategoryChannel = nc.SlashOption(
                description="La catégorie où les tickets seront créés.",
                required=True
                ),
            support_role: nc.Role = nc.SlashOption(
                description="Le rôle qui aura accès aux tickets.",
                required=True
            )
            ):
        await interaction.guild.fetch_roles()

        if not TicketUtils.user_has_permission(interaction):
            await interaction.send(
                    "Désolé mon grand, mais tu n'as pas la permission de faire ça.",
                    )
            return

        if tc.get_ticket_category():
            await TicketUtils.handle_existing_ticket_system(interaction, ticket_category, support_role)
        else:
            await TicketUtils.setup_new_ticket_system(interaction, ticket_category, support_role)

    @nc.slash_command(description="Accepter une carte étudiante.")
    async def accepter_etudiant(
        self,
        interaction: nc.Interaction,
        ecole: str = nc.SlashOption(
            description="Le nom de l'école de l'étudiant.",
            required=True,
            choices=sc.get_all_schools().keys()
            )
    ):
        if interaction.channel.category_id == tc.get_ticket_category():

            user = await interaction.guild.fetch_member(int(interaction.channel.topic))

            if not sc.get_school(ecole):
                await interaction.send("L'école n'a pas été configurée.")
                return
            
            role = await interaction.guild.fetch_role(sc.get_school(ecole))

            await user.add_roles(role)

            await interaction.send("Etudiant accepté !\n-# Ce channel sera supprimé dans 5 secondes.")

            try:
                user.send("Votre statut étudiant a été accepté !")
            except nc.Forbidden:
                pass

            sleep(5)

            await interaction.channel.delete()



def setup(bot):
    bot.add_cog(ManageTicketCommand(bot))

