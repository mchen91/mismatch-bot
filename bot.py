import os

from interactions import Client, Intents

from commands.general_commands import register_general_commands
from commands.owner_commands import register_owner_commands

bot = Client(token=os.environ["DISCORD_TOKEN"], intents=Intents.ALL)

register_general_commands(bot)
register_owner_commands(bot)
bot.start()
