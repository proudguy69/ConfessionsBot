from discord.ext.commands import Cog, Bot
from discord.app_commands import command, describe
from discord import Interaction, Embed, Attachment

from database.setupdb import get_setup
from database.confessiondb import create_confession


class ConfessionExtension(Cog):
    def __init__(self, bot:Bot):
        self.bot = bot
        super().__init__()
    
    @command(name='confess', description='create a confession')
    @describe(confession="The thing you want to confess", image="an immage to attach to the confession, permissions are required")
    async def confess(self, interaction:Interaction, confession:str, image:Attachment=None):
        await interaction.response.defer(ephemeral=True)
        server_setup = get_setup(interaction.guild_id)
        
        # fall out clauses
        if not server_setup.confession_channel: return await interaction.followup.send("The server has no confession channel setup!", ephemeral=True)
        
        can_confess = True
        can_image_perms = True
        if server_setup.confession_permissions:
            can_confess = False
            can_image_perms = False
            for role_id in server_setup.confession_permissions.get('role_ids', []):
                if int(role_id) in [r.id for r in interaction.user.roles]:
                    can_confess = True
                    break
            for role_id in server_setup.image_permissions:
                if int(role_id) in [r.id for r in interaction.user.roles]:
                    can_image_perms = True
                    break

        if not can_confess: return await interaction.followup.send("You do not have the permissions to confess!", ephemeral=True)
        if image and not can_image_perms: return await interaction.followup.send("You do not have permissions to attach images!", ephemeral=True)

        confession_channel = interaction.guild.get_channel(server_setup.confession_channel)
        confession_embed = Embed(title="New confession", description=confession)
        if image: confession_embed.set_image(url=image.url)
        

        # create a documentable confession obj
        confession_obj = create_confession(interaction.guild_id,interaction.user.id,None,None,confession,image.url if image else None)

        confession_embed.set_author(name=f"Anonymous Confession #{confession_obj._id}", icon_url=interaction.guild.icon.url)

        msg = await confession_channel.send(embed=confession_embed)
        await interaction.followup.send(f"Your confession has been posted here: {msg.jump_url}", ephemeral=True)
        if not server_setup.logging_channel: return
        logging_channel = interaction.guild.get_channel(server_setup.logging_channel)
        confession_embed.add_field(name='Sent By', value=f"{interaction.user.mention} `({interaction.user.id})`\n\nLink:{msg.jump_url}")
        confession_embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        log_msg = await logging_channel.send(embed=confession_embed)

        confession_obj.update({"$set":{"message_id":msg.id,"log_id":log_msg.id}})
    @confess.error
    async def confession_error(self, interaction:Interaction, error):
            await interaction.followup.send("An error occured! report below to the owner!")
            await interaction.channel.send(f"The following error occured:\n\n```{error}```")
        





    








async def setup(bot:Bot):
    await bot.add_cog(ConfessionExtension(bot))