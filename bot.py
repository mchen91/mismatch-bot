import os

from discord.ext import commands
from discord.ext.commands.context import Context
from discord_slash import SlashCommand

from commands.general_commands import GeneralSlashCommand
from commands.owner_commands import OwnerSlashCommand


bot = commands.Bot(command_prefix='-lol')
SlashCommand(bot, sync_commands=True)


@bot.event
async def on_command_error(ctx: Context, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


bot.add_cog(GeneralSlashCommand(bot))
bot.add_cog(OwnerSlashCommand(bot))
bot.run(os.environ["DISCORD_TOKEN"])
