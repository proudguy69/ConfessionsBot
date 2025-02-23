from discord.ext.commands import Cog, Bot
from discord.app_commands import Group, describe, default_permissions
from discord import Interaction, TextChannel


from database.setupdb import get_setup, Setup

class SetupExtension(Cog):
    
    setup = Group(name="setup", description="a group of setup commands")
    setup_channel = Group(name="channel", description="a group of setup commands to configure channels", parent=setup)

    @setup_channel.command(name="confession", description="sets up the confession channel")
    @default_permissions(administrator=True)
    @describe(channel="The channel you want confessions to be posted too")
    async def setup_channel_confession(self, interaction:Interaction, channel:TextChannel):
        await interaction.response.defer(ephemeral=True)
        setup = get_setup(interaction.guild_id)
        setup.update({"$set":{"confession_channel":channel.id}})
        await interaction.followup.send(f"Done! All confessions will be posted too: {channel.mention}")




async def setup(bot:Bot):
    await bot.add_cog(SetupExtension())