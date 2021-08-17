import os

from discord.ext import commands

from commands.constants import COMMAND_PREFIX
from commands.general_commands import GeneralCommand
from commands.owner_commands import OwnerCommand


bot = commands.Bot(command_prefix=COMMAND_PREFIX)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


bot.add_cog(GeneralCommand(bot))
bot.add_cog(OwnerCommand(bot))
bot.run(os.environ["DISCORD_TOKEN"])
