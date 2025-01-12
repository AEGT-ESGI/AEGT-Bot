import nextcord as nc
from nextcord.ext import commands
from nextcord.ui import Button, View
from time import sleep
from config import TicketConfig

tc = TicketConfig()


class TicketUtils:
    @staticmethod
    def user_has_permission(interaction: nc.Interaction) -> bool:
        return (
                interaction.user.top_role.permissions.manage_channels or
                interaction.user.top_role.permissions.administrator or
                interaction.user.id == interaction.guild.owner_id
                )

    @staticmethod
    async def handle_existing_ticket_system(interaction: nc.Interaction, ticket_category: nc.CategoryChannel):
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

        view.interaction_check = lambda i: TicketUtils.allow_ticket_creation(i, ticket_category)

        await interaction.send(
                "Il y a déjà un système de tickets, tu veux vraiment le supprimer pour en créer un nouveau ? <:OHHHH:1287740128806309930>",
                view=view
                )

    @staticmethod
    async def setup_new_ticket_system(interaction: nc.Interaction, ticket_category: nc.CategoryChannel):
        tc.set_ticket_channel(interaction.channel.id)
        tc.set_ticket_category(ticket_category.id)

        await interaction.send(
                "Le système de tickets a été superbement configuré ! <:yay:1274376322847739935>"
                )

        await TicketUtils.send_ticket_embed(interaction.channel)

        sleep(3)
        await interaction.delete_original_message()

    @staticmethod
    async def allow_ticket_creation(interaction: nc.Interaction, ticket_category: nc.CategoryChannel):
        if interaction.data["custom_id"] == "delete_ticket":
            tc.set_ticket_channel(interaction.channel.id)
            tc.set_ticket_category(ticket_category.id)

            await interaction.message.edit(
                    "Le système de tickets a été superbement configuré ! <:yay:1274376322847739935>",
                    view=None
                    )

            await TicketUtils.send_ticket_embed(interaction.channel)

            sleep(3)
            await interaction.message.delete()
        else:
            await interaction.message.edit(
                    "On fera la configuration plus tard. <:miamchoco:1216663553722023966>",
                    view=None
                    )

            sleep(3)
            await interaction.message.delete()

    @staticmethod
    async def send_ticket_embed(channel: nc.TextChannel):
        view = View()
        view.add_item(Button(
            style=nc.ButtonStyle.primary,
            label="Créer un ticket",
            custom_id="create_ticket"
            ))

        embed = nc.Embed(
                title="Ticket d'entrée <:petitefrog:1216663533928845322>",
                description="Pour rentrer sur le serveur, merci d'ouvrir un ticket et répondre aux questions ! <:yay:1274376322847739935>",
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
                )
            ):
        await interaction.guild.fetch_roles()

        if not TicketUtils.user_has_permission(interaction):
            await interaction.send(
                    "Eh oh, tu tentes de faire quoi ? Pas touche à cette commande ! <:attaque:1216663550282694717>"
                    )
            return

        if tc.get_ticket_channel():
            await TicketUtils.handle_existing_ticket_system(interaction, ticket_category)
        else:
            await TicketUtils.setup_new_ticket_system(interaction, ticket_category)


def setup(bot):
    bot.add_cog(ManageTicketCommand(bot))

