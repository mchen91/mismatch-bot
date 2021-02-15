import os
from discord.ext import commands

MY_ID = 97904188918345728

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == MY_ID
    return commands.check(predicate)

bot = commands.Bot(command_prefix="-mm ")


@bot.command()
@is_me()
async def update(ctx, character_name, stage_name, time_string, player_name, video_link):
    from use_cases.records import add_record

    # TODO: partial targets
    add_record(
        character_name=character_name,
        stage_name=stage_name,
        player_name=player_name,
        time_string=time_string,
        video_link=video_link,
    )
    await ctx.send(f"Added {character_name}/{stage_name} - {time_string} by {player_name} at {video_link}")


bot.run(os.environ["DISCORD_TOKEN"])
