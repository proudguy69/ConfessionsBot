from database.database import SETUP
from discord import Embed, Member

class Setup:
    def __init__(self, data:dict):
        self.guild_id = data.get("guild_id", None)
        self.confession_channel = data.get("confession_channel", None)
        self.logging_channel = data.get("logging_channel", None)
        self.image_permissions = data.get("image_permissions", [])
        self.confession_permissions:dict = data.get("confession_permissions", {})
        self.message_content = data.get("message_content", '')
        self.message_embed:dict = data.get("message_embed", {"title":"New Confession!","description":"{user.mention} submitted a new confession:\n\n{confession}","color":0xffa1dc,"author":{"name":"{user.name}","icon_url":"{user.avatar.url}"}})
        self.embed = self.setup_embed()
        if not data.get('message_embed'):
            # update the database
            self.update({"$set":{"message_embed":self.message_embed}})
    
    def update(self, data):
        SETUP.update_one({"guild_id":self.guild_id}, data, upsert=True)
        data = SETUP.find_one({"guild_id":self.guild_id})
        self.__init__(data)
    
    # for embed of the current settings
    def setup_embed(self) -> Embed:
        """Creates an embed with all the attributes of this class

        Returns:
            Embed: a discord.Embed
        """
        confession_channel = f"<#{self.confession_channel}>" if self.confession_channel else None
        logging_channel = f"<#{self.logging_channel}>" if self.logging_channel else None
        confession_permissions = "`[" + self.confession_permissions.get('mode','') + "ed]` " +  ", ".join(f"<@&{r_id}>" for r_id in self.confession_permissions.get("role_ids",[])) if self.confession_permissions else None
        image_permissions = ", ".join(f"<@&{r_id}>" for r_id in self.image_permissions) if self.image_permissions else None
        message_content = self.message_content if self.message_content else None

        description = f"""
        `Confessions Channel:` {confession_channel}
        `Logging Channel`: {logging_channel}
        `Confessions Permissions`: {confession_permissions}
        `Image Permissions`: {image_permissions}
        `Message Content:` {message_content}

        use `/setup message embed` to see the embeds configuration
        """

        setup_embed = Embed(title="Setup Configuration", description=description)
        return setup_embed

    def create_embed(self, user:Member, confession:str) -> Embed:
        """Creates an embed from the message_embed attribute

        Returns:
            Embed: a discord.Embed
        """

        embed_data = self.message_embed
        
        if embed_data.get('author'):
            embed_data['author']['name'] = embed_data['author']['name'].format(user=user)
            if embed_data['author'].get('icon_url'): embed_data['author']['icon_url'] = embed_data['author']['icon_url'].format(user=user)
            if embed_data['author'].get('url'): embed_data['author']['url'] = embed_data['author']['url'].format(user=user)

        embed_data['description'] = embed_data['description'].format(user=user, confession=confession)
        confession_embed = Embed.from_dict(embed_data)
        return confession_embed






def get_setup(guild_id:int) -> Setup:
    data = SETUP.find_one({"guild_id":guild_id})
    if data == None: data = {"guild_id":guild_id}
    return Setup(data)

