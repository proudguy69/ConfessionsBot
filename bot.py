from discord.ext.commands import Bot, Context, command
from discord import Intents

from settings import TOKEN


class ConfessionBot(Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=Intents.all())

    async def setup_hook(self):
        pass



bot = ConfessionBot()


bot.run(TOKEN)