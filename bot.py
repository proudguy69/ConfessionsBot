from discord.ext.commands import Bot, Context, is_owner
from discord import Intents, utils
import logging

from settings import TOKEN

utils.setup_logging()

class ConfessionBot(Bot):
    def __init__(self):
        super().__init__(command_prefix='-', intents=Intents.all())
        self.logger = logging.getLogger('Bot')
        self.custom_extensions:list[str] = ["cogs.setup"]

    async def setup_hook(self):
        self.logger.info("Runnings setup hook")
        await self.load_extensions()

    async def load_extensions(self): 
        self.logger.info("Loading Extensions")
        for custom_extension in self.custom_extensions:
            self.logger.info(f"Loading Extension: {custom_extension}")
            await self.load_extension(custom_extension)

    async def reload_extensions(self):
        self.logger.info("Reloading Extensions")
        for custom_extension in self.custom_extensions:
            self.logger.info(f"Hot Reloading Extension: {custom_extension}")
            await self.reload_extension(custom_extension)

bot = ConfessionBot()
tree = bot.tree

@bot.command()
@is_owner()
async def sync(context:Context):
    bot.logger.warning("Syncing Application Commands")
    message = await context.send("Syncing application commands.")
    await tree.sync()
    await message.edit(content="Done syncing application commands.")
    bot.logger.warning("Syncing Application Commands Completed")


@bot.command()
@is_owner()
async def reload(context:Context):
    message = await context.send("Reloading extensions.")
    await bot.reload_extensions()
    await message.edit(content="Done reloading extensions.")
    bot.logger.info("Reloading Extensions Completed")




bot.run(TOKEN)