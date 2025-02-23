from discord.ext.commands import Cog, Bot
from discord.app_commands import Command

class Setup(Cog):
    pass



async def setup(bot:Bot):
    await bot.add_cog(Setup())