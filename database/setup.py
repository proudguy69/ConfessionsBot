from database.database import SETUP

class Setup:
    def __init__(self, data:dict):
        self.guild_id = data.get("guild_id", None)
        self.confession_channel = data.get("confession_channel", None)
        self.logging_channel = data.get("logging_channel", None)
        self.image_permissions = data.get("image_permissions", [])
        self.confession_permissions = data.get("confession_permissions", [])
        self.message_content = data.get("message_content", '')
        self.message_embed = data.get("message_embed", {})
    
    def update(self, data):
        SETUP.update_one({{"guild_id":self.guild_id}}, data, upsert=True)
        data = SETUP.find_one({"guild_id":self.guild_id})
        self.__init__(data)





def get_setup(guild_id:int) -> Setup:
    data = SETUP.find_one({"guild_id":guild_id})
    if data == None: data = {"guild_id":guild_id}
    return Setup(data)

