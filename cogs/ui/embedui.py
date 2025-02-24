from discord.ui import View, button, Modal, TextInput
from discord import Button, ButtonStyle, Interaction, TextStyle, Embed

from database.setupdb import get_setup, Setup


class CreateEmbedView(View):
    def __init__(self, *, timeout = 300):
        super().__init__(timeout=timeout)
    
    @button(label="Yes", style=ButtonStyle.green)
    async def create_embed(self, interaction:Interaction, button:Button):
        # we are gonna change out of THIS view and set to the embed creation
        server_setup = get_setup(interaction.guild_id)
        await interaction.response.edit_message(content="Below is the embed to edit, press any of the buttons to edit the embed",
                                                embed=server_setup.create_embed(),
                                                view=EditEmbedView())
        

    @button(label="No", style=ButtonStyle.red)
    async def skip_creation(self, interaction:Interaction, button:Button):
        self.children[0].disabled = True
        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send("Okay! if you change your mind run this view again and press yes")




class EmbedModal(Modal):
    def __init__(self, original_interaction:Interaction):
        self.original_interaction = original_interaction
        super().__init__(title="Edit Embed Body", timeout=500)
    
    title = TextInput(label="title", style=TextStyle.short, placeholder="the title of the embed")
    color = TextInput(label="color", style=TextStyle.short, placeholder="the color of the embed, in #ffa1dc format", max_length=7, min_length=6, default="#ffa1dc", required=False)
    description = TextInput(label="description", style=TextStyle.paragraph, placeholder="the description of the embed, varibles allowed")
    footer = TextInput(label="footer", style=TextStyle.short, placeholder="the footer of the embed", required=False)

    async def on_submit(self, interaction:Interaction):
        await interaction.response.defer()
        server_setup = get_setup(interaction.guild_id)
        server_setup.update({"$set":{
            "message_embed.title":self.title,
            "message_embed.description":self.description,
            "message_embed.color":self.color,
            "message_embed.footer":self.footer if self.footer else '',
        }})
        new_embed = server_setup.create_embed()
        self.original_interaction.edit_original_response(embed=new_embed)





class EditEmbedView(View):
    def __init__(self):
        super().__init__(timeout=None) # not persistant after bot reset
    
    @button(label='edit embed body', custom_id='embed_body', style=ButtonStyle.gray)
    async def edit_embed_body(self, interaction:Interaction, button:Button):
        await interaction.response.send_modal(EmbedModal(interaction))

