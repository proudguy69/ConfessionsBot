from discord.ui import View, button, Modal, TextInput
from discord import Button, ButtonStyle, Interaction, TextStyle, Embed

from database.setupdb import get_setup, Setup



class EditEmbedBodyModal(Modal):
    def __init__(self, original_interaction:Interaction):
        self.original_interaction = original_interaction
        super().__init__(title="Edit Embed Body", timeout=500)
        server_setup = get_setup(original_interaction.guild_id)
    
        self.embed_title = TextInput(label="title", style=TextStyle.short, placeholder="the title of the embed", default=server_setup.message_embed.get('title', ''))
        self.color = TextInput(label="color", style=TextStyle.short, placeholder="the color of the embed, in #ffa1dc format", default=hex(server_setup.message_embed.get('color', '')).replace('0x','#'), max_length=7, min_length=6, required=False)
        self.description = TextInput(label="description", style=TextStyle.paragraph, placeholder="the description of the embed, varibles allowed", default=server_setup.message_embed.get('description', ''))
        self.footer = TextInput(label="footer", style=TextStyle.short, placeholder="the footer of the embed", required=False, default=server_setup.message_embed.get('footer', {}).get('text', ''))

        self.add_item(self.embed_title)
        self.add_item(self.color)
        self.add_item(self.description)
        self.add_item(self.footer)

    async def on_submit(self, interaction:Interaction):
        await interaction.response.defer()
        server_setup = get_setup(interaction.guild_id)
        update_data = {
            "message_embed.title":self.embed_title.value,
            "message_embed.description":self.description.value,
            "message_embed.color":int(self.color.value.replace('#',''), base=16),
        }
        
        if self.footer:
            update_data["message_embed.footer.text"] = self.footer.value
        else:
            # remove footer if not provided
            server_setup.update({"$unset":{"message_embed.footer":''}})


        server_setup.update({"$set":update_data})
        new_embed = server_setup.create_embed(interaction.user, confession="example confession")
        await self.original_interaction.edit_original_response(embed=new_embed)


class EditEmbedAuthorModal(Modal):
    def __init__(self, original_interaction:Interaction):
        super().__init__(title="Edit Embed Author", timeout=None, custom_id="edit_embed_author")
        self.original_interaction = original_interaction
        server_setup = get_setup(original_interaction.guild_id)
        self.name = TextInput(label="name", placeholder="the name of the author", required=False, default=server_setup.message_embed.get('author',{}).get('name',''))
        self.url = TextInput(label="url", placeholder="the url of the author (this is clickable)", required=False, default=server_setup.message_embed.get('author',{}).get('url',''))
        self.icon_url = TextInput(label="icon_url", placeholder="the icon url of the author (use {user.avatar.url} to get the avatar url)", required=False, default=server_setup.message_embed.get('author',{}).get('icon_url',''))

        self.add_item(self.name)
        self.add_item(self.url)
        self.add_item(self.icon_url)
    
    async def on_submit(self, interaction:Interaction):
        await interaction.response.defer()
        server_setup = get_setup(interaction.guild_id)
        if not self.name.value:
            server_setup.update({"$unset":{"message_embed.author":''}})
            new_embed = server_setup.create_embed(user=interaction.user, confession='example confession')
            await self.original_interaction.edit_original_response(embed=new_embed)
            return await interaction.followup.send("You need to set the name field at least! or leave it empty to keep it removed")
        

        update_data = {
            "message_embed.author.name":self.name.value,
        }
        
        if self.url:
            update_data["message_embed.author.url"] = self.url.value
        if self.icon_url:
            update_data["message_embed.author.icon_url"] = self.icon_url.value

        server_setup.update({"$set":update_data})
        new_embed = server_setup.create_embed(user=interaction.user, confession="example confession")
        await self.original_interaction.edit_original_response(embed=new_embed)


class EditEmbedView(View):
    def __init__(self):
        super().__init__(timeout=None) # not persistant after bot reset
    
    @button(label='Edit Embed Body', custom_id='embed_body', style=ButtonStyle.gray)
    async def edit_embed_body(self, interaction:Interaction, button:Button):
        await interaction.response.send_modal(EditEmbedBodyModal(interaction))
    
    @button(label='Edit Embed Author', custom_id='embed_author', style=ButtonStyle.gray)
    async def edit_embed_author(self, interaction:Interaction, button:Button):
        await interaction.response.send_modal(EditEmbedAuthorModal(interaction))

