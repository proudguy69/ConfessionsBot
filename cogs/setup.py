from discord.ext.commands import Cog, Bot
from discord.app_commands import Group, describe, default_permissions
from discord import Interaction, TextChannel

from database.setupdb import get_setup, Setup

from enum import Enum

class Mode(Enum):
    whitelist = "whitelist"
    blacklist = "blacklist"

class SetupExtension(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    setup = Group(name="setup", description="a group of setup commands")
    setup_channel = Group(name="channel", description="a group of setup commands to configure channels", parent=setup)
    setup_permissions = Group(name="permissions", description="a group of setup commands to configure confession permissions", parent=setup)
    setup_message = Group(name="message", description="a group of setup commands to configure confession message", parent=setup)

    @setup.command(name="view", description="view the servers current setup/settings")
    @default_permissions(administrator=True)
    @describe(public="weather or not you want the response of this command to be hidden or not")
    async def setup_view(self, interaction:Interaction, public:bool=False):
        ephemeral = (not public)
        await interaction.response.defer(ephemeral=ephemeral)
        server_setup = get_setup(interaction.guild.id)
        await interaction.followup.send(embed=server_setup.embed, ephemeral=ephemeral)


    # setup channel commands
    @setup_channel.command(name="confession", description="sets up the confession channel")
    @default_permissions(administrator=True)
    @describe(channel="The channel you want confessions to be posted too")
    async def setup_channel_confession(self, interaction:Interaction, channel:TextChannel):
        await interaction.response.defer(ephemeral=True)
        setup = get_setup(interaction.guild_id)
        setup.update({"$set":{"confession_channel":channel.id}})
        await interaction.followup.send(f"Done! All confessions will be posted too: {channel.mention}")
    
    @setup_channel.command(name="logging", description="sets up the logging channel to log confessions")
    @default_permissions(administrator=True)
    @describe(channel="The channel you want your confession logs to be posted too")
    async def setup_channel_logging(self, interaction:Interaction, channel:TextChannel):
        await interaction.response.defer(ephemeral=True)
        setup = get_setup(interaction.guild_id)
        setup.update({"$set":{"logging_channel":channel.id}})
        await interaction.followup.send(f"Done! All connfession logs will be posted too: {channel.mention}")

    
    # setup permission commands
    @setup_permissions.command(name="confessions", description="sets up what roles can or cant run the /confess command based on whitelist/blacklist")
    @default_permissions(administrator=True)
    @describe(roles="list of roles to set up, must be seperated by a comma", mode="weather or not the roles provided should be whitelisted (can use the command) or blacklisted (cant use the command)")
    async def setup_permission_confession(self, interaction:Interaction, roles:str, mode:Mode):
        await interaction.response.defer(ephemeral=True)
        str_role_ids = roles.replace('<@&', '').replace('>', '').replace(' ', '').split(',')
        int_role_ids = [int(r) for r in str_role_ids]
        setup = get_setup(interaction.guild_id)
        setup.update({"$set":{"confession_permissions":{"mode":mode.value,"role_ids":int_role_ids}}})
        roles_msg = ", ".join(f'<@&{role_id}>' for role_id in int_role_ids)
        message  = f"Succesfully {mode.value}ed: {roles_msg}"
        await interaction.followup.send(message, ephemeral=True)
    @setup_permission_confession.error
    async def setup_permission_confession_error(self, interaction:Interaction, error):
        self.bot.logger.error(f"Ignoring Exception in cogs.setup.setup_permission_confession: {error}")
        await interaction.followup.send(f"An error occured! did you forget to seperate roles with a comma?, full error:\n```cmd\n{error}\n```\nThis error does NOT represent what YOU may have done wrong, you still may have forgotten a comma even if it says \"mongo db overflow error\"")


    @setup_permissions.command(name="image", description="sets up what roles can or cant run the /confess with image based on whitelist")
    @default_permissions(administrator=True)
    @describe(roles="list of roles to set up, must be seperated by a comma")
    async def setup_permission_image(self, interaction:Interaction, roles:str):
        await interaction.response.defer(ephemeral=True)
        str_role_ids = roles.replace('<@&', '').replace('>', '').replace(' ', '').split(',')
        int_role_ids = [int(r) for r in str_role_ids]
        setup = get_setup(interaction.guild_id)
        setup.update({"$set":{"image_permissions":int_role_ids}})
        roles_msg = ", ".join(f'<@&{role_id}>' for role_id in int_role_ids)
        message  = f"Succesfully whitelisteded: {roles_msg}"
        await interaction.followup.send(message, ephemeral=True)
    @setup_permission_image.error
    async def setup_permission_image_error(self, interaction:Interaction, error):
        self.bot.logger.error(f"Ignoring Exception in cogs.setup.setup_permission_image: {error}")
        await interaction.followup.send(f"An error occured! did you forget to seperate roles with a comma?, full error:\n```cmd\n{error}\n```\nThis error does NOT represent what YOU may have done wrong, you still may have forgotten a comma even if it says \"mongo db overflow error\"")
        


    # setup message commands
    @setup_message.command(name="content", description="sets the content of the message (NOT THE EMBED DESCRIPTION)")
    @default_permissions(administrator=True)
    @describe(content="the content for the message")
    async def setup_message_content(self, interaction:Interaction, content:str):
        await interaction.response.defer(ephemeral=True)
        setup = get_setup(interaction.guild_id)
        setup.update({"$set":{"message_content":content}})
        await interaction.followup.send(f"Done! The confession message is now:\n\n{content}")
    
    @setup_message.command(name="embed", description="sets up the confession embed")
    @default_permissions(administrator=True)
    async def setup_message_embed(self, interaction:Interaction):
        await interaction.response.defer(ephemeral=True)
        setup = get_setup(interaction.guild_id)
        if not setup.message_embed:
            # creation view
            await interaction.followup.send("It looks like there is not an embed, would you like to setup one?")
            return
        await interaction.followup.send(setup.message_embed)



    



async def setup(bot:Bot):
    await bot.add_cog(SetupExtension(bot))