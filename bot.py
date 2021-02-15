import os
from discord.ext import commands

MY_ID = 97904188918345728

bot = commands.Bot(command_prefix="-mm ")


def is_me():
    def predicate(ctx):
        return ctx.message.author.id == MY_ID

    return commands.check(predicate)


@bot.command()
@is_me()
async def set(ctx, character_name, stage_name, time_string, player_name, video_link):
    from use_cases.records import add_record

    # TODO: partial targets
    add_record(
        character_name=character_name,
        stage_name=stage_name,
        player_name=player_name,
        time_string=time_string,
        video_link=video_link,
    )
    await ctx.send(
        f"Added {character_name}/{stage_name} - {time_string} by {player_name} at {video_link}"
    )


@bot.command()
async def get(ctx, character_name, stage_name):
    from use_cases.records import get_record
    from use_cases.frame_conversion import frames_to_time_string

    record = get_record(character_name=character_name, stage_name=stage_name)

    if record:
        players_string = ",".join(player.name for player in record.players) or "Anonymous"
        video_link_string = f"at {record.video_link}" if record.video_link else ""
        record_value = (
            f"{record.partial_targets} targets"
            if record.partial_targets
            else frames_to_time_string(record.time)
        )
        msg = f"{character_name}/{stage_name} - {record_value} by {players_string} {video_link_string}"
    else:
        msg = f"No record found for {character_name}/{stage_name}"
    await ctx.send(msg)


bot.run(os.environ["DISCORD_TOKEN"])
