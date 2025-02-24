from database.database import CONFESSIONS


class Confession:
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get("guild_id", None)
        self.author_id = data.get("author_id", None)
        self.confession = data.get("confession", None)
        self.image_url = data.get("image_url", None)
        self.message_id = data.get("message_id", None)
        self.log_id = data.get("log_id", None)
        self.log_history = data.get("log_history", [])
    
    def update(self, data):
        CONFESSIONS.update_one({"_id":self._id}, data, upsert=True)
        new_data = CONFESSIONS.find_one({"_id":self._id})
        self.__init__(new_data)


def create_confession(guild_id:int, author_id:int, message_id:int|None, log_id:int|None, confession:str, image_url:str=None) -> Confession:
    """Inserts a confession into the database

    Args:
        guild_id (int): the id of the guild
        author_id (int): the id of the author of the confession
        message_id (int): the id of the message that was sent in the confession channel
        log_id (int): the id of the message that was sent in the logging channel
        confession (str): the text of the confession
        image_url (str): the image that was attached to the confession

    Returns:
        Confession: the confession database object
    """
    _id = len(list(CONFESSIONS.find())) +1
    data = {
        "_id":_id,
        "guild_id":guild_id,
        "author_id":author_id,
        "confession":confession,
        "image_url":image_url,
        "message_id":message_id,
        "log_id":log_id,
        "log_history":[],
    }
    CONFESSIONS.insert_one(data)
    return Confession(data)
