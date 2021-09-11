import os

from discord.ext import commands
from discord_slash import SlashCommand

from commands.constants import COMMAND_PREFIX
from commands.general_commands import GeneralCommand, GeneralSlashCommand
from commands.owner_commands import OwnerCommand


bot = commands.Bot(command_prefix=COMMAND_PREFIX)
SlashCommand(bot, sync_commands=True)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


bot.add_cog(GeneralCommand(bot))
bot.add_cog(OwnerCommand(bot))
bot.add_cog(GeneralSlashCommand(bot))
bot.run(os.environ["DISCORD_TOKEN"])
