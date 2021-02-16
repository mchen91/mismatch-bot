import os
from discord.ext import commands

from db import get_session

MY_ID = 97904188918345728
COMMAND_PREFIX = "-mm "

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


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
async def wr(ctx, *, char_and_stage):
    from use_cases.character import get_character_by_name
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_record
    from use_cases.stage import get_stage_by_name

    combo_array = char_and_stage.split("/")
    if len(combo_array) != 2:
        await ctx.send(
            "syntax: {COMMAND_PREFIX}<char>/<stage>. e.g. `-mm young link/samus`"
        )
        return
    character_name, stage_name = [s.strip() for s in combo_array]

    session = get_session()
    try:
        character = get_character_by_name(character_name, session)
    except ValueError as error:
        await ctx.send(str(error))
        return
    try:
        stage = get_stage_by_name(stage_name, session)
    except ValueError as error:
        await ctx.send(str(error))
        return
    record = get_record(session=session, character=character, stage=stage)

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
        msg = f"No record found for {character.name}/{stage.name}"
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


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


bot.run(os.environ["DISCORD_TOKEN"])
