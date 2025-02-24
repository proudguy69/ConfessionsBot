from discord.ext.commands import Cog, Bot
from discord.app_commands import command, describe
from discord import Interaction, Embed

from database.setupdb import get_setup


class ConfessionExtension(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        super().__init__()
    
    @command(name='confess', description='create a confession')
    @describe(confession="The thing you want to confess")
    async def confess(self, interaction:Interaction, confession:str):
        await interaction.response.defer(ephemeral=True)
        server_setup = get_setup(interaction.guild_id)
        
        # fall out clauses
        if not server_setup.confession_channel: return await interaction.followup.send("The server has no confession channel setup!", ephemeral=True)
        
        can_confess = True
        if server_setup.confession_permissions:
            can_confess = False
            for role_id in server_setup.confession_permissions.get('role_ids', []):
                if int(role_id) in [r.id for r in interaction.user.roles]:
                    can_confess = True
                    break

        if not can_confess: return await interaction.followup.send("You do not have the permissions to confess!", ephemeral=True)

        confession_channel = interaction.guild.get_channel(server_setup.confession_channel)
        confession_embed = Embed(title="New confession", description=confession)
        confession_embed.set_author(name="Anonymous Confession", icon_url=interaction.guild.icon.url)
        msg = await confession_channel.send(embed=confession_embed)
        await interaction.followup.send(f"Your confession has been posted here: {msg.jump_url}", ephemeral=True)
        if not server_setup.logging_channel: return
        logging_channel = interaction.guild.get_channel(server_setup.logging_channel)
        await logging_channel.send(embed=server_setup.create_embed(user=interaction.user, confession=confession))





    








async def setup(bot:Bot):
    await bot.add_cog(ConfessionExtension(bot))