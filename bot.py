import os
from discord.ext import commands

from db import get_session

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

    session = get_session()
    # TODO: partial targets
    record = add_record(
        session=session,
        character_name=character_name,
        stage_name=stage_name,
        player_name=player_name,
        time_string=time_string,
        video_link=video_link,
    )
    await ctx.send(
        f"Added {record.character.name}/{record.stage.name} - {time_string} by {player_name} at {video_link}"
    )
    session.close()


@bot.command()
async def get(ctx, character_name, stage_name):
    from use_cases.records import get_record
    from use_cases.frame_conversion import frames_to_time_string

    session = get_session()
    record = get_record(
        session=session, character_name=character_name, stage_name=stage_name
    )

    if record:
        players_string = (
            ",".join(player.name for player in record.players) or "Anonymous"
        )
        video_link_string = f"at {record.video_link}" if record.video_link else ""
        record_value = (
            f"{record.partial_targets} targets"
            if record.partial_targets
            else frames_to_time_string(record.time)
        )
        msg = f"{record.character.name}/{record.stage.name} - {record_value} by {players_string} {video_link_string}"
    else:
        msg = f"No record found for {character_name}/{stage_name}"
    await ctx.send(msg)
    session.close()


@bot.command()
@is_me()
async def aliasc(ctx, aliased_name, known_name):
    from use_cases.aliases import add_char_stage_alias

    session = get_session()
    try:
        new_alias = add_char_stage_alias(
            session=session, aliased_name=aliased_name, known_name=known_name
        )
    except ValueError as error:
        msg = str(error)
    else:
        if new_alias.character and new_alias.stage:
            aliased = new_alias.character.name
        elif new_alias.character:
            aliased = f"only character {new_alias.character}"
        else:
            aliased = f"only stage {new_alias.stage}"
        msg = f"Aliased {aliased_name} to {aliased}"
    await ctx.send(msg)
    session.close()


@bot.command()
@is_me()
async def aliasp(ctx, aliased_name, known_name):
    from use_cases.aliases import add_player_alias

    session = get_session()
    try:
        new_alias = add_player_alias(
            session=session, aliased_name=aliased_name, known_name=known_name
        )
    except ValueError as error:
        msg = str(error)
    else:
        msg = f"Aliased {aliased_name} to {new_alias.player.name}"
    await ctx.send(msg)
    session.close()


bot.run(os.environ["DISCORD_TOKEN"])
