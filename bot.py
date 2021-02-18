import os
from discord import Embed
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
async def add(ctx, character_name, stage_name, time_string, player_name, video_link):
    from use_cases.character import get_character_by_name
    from use_cases.frame_conversion import time_string_to_frames
    from use_cases.player import get_player_by_name
    from use_cases.records import add_record
    from use_cases.stage import get_stage_by_name

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
    try:
        player = get_player_by_name(player_name, session)
    except ValueError as error:
        await ctx.send(str(error))
        return

    is_partial_target_record = "target" in time_string
    if is_partial_target_record:
        time = None
        partial_targets = int(time_string[0])
    else:
        time = time_string_to_frames(time_string)
        partial_targets = None

    record = add_record(
        session=session,
        character=character,
        stage=stage,
        player=player,
        time=time,
        partial_targets=partial_targets,
        video_link=video_link,
    )
    await ctx.send(
        f"Added {record.character.name}/{record.stage.name} - {time_string} by {player.name} at {video_link}"
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
            f"{record.partial_targets} target"
            if record.partial_targets == 1
            else f"{record.partial_targets} targets"
            if record.partial_targets is not None
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
            aliased = f"only character {new_alias.character.name}"
        else:
            aliased = f"only stage {new_alias.stage.name}"
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


@bot.command(
    aliases=["char", "char-records", "character", "charrecords", "character-records"]
)
async def character_records(ctx, character_name):
    from use_cases.character import get_character_by_name
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_records_by_character

    session = get_session()
    character = get_character_by_name(character_name, session)
    records = get_records_by_character(session=session, character=character)
    description_lines = [f"{character.name} Character Records"]
    for record in records:
        record_string = (
            f"{record.partial_targets} target"
            if record.partial_targets == 1
            else f"{record.partial_targets} targets"
            if record.time is None
            else frames_to_time_string(record.time)
        )
        if record.video_link:
            record_string = f"[{record_string}]({record.video_link})"
        players = (
            ",".join(player.name for player in record.players)
            if record.players
            else "Anonymous"
        )
        description_lines.append(f"{record.stage.name} - {record_string} - {players}")
    total_frames = sum(
        0 if (record.time is None or record.stage.position > 24) else record.time
        for record in records
    )
    description_lines.append(f"25 Stage Total: {frames_to_time_string(total_frames)}")
    embed = Embed()
    embed.description = "\n".join(description_lines)
    await ctx.send(embed=embed)
    session.close()


@bot.command(aliases=["stage", "stagerecords", "stage-records"])
async def stage_records(ctx, stage_name):
    from use_cases.stage import get_stage_by_name
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_records_by_stage

    session = get_session()
    stage = get_stage_by_name(stage_name, session)
    records = get_records_by_stage(session=session, stage=stage)
    description_lines = [f"{stage.name} Stage Records"]
    for record in records:
        record_string = (
            f"{record.partial_targets} target"
            if record.partial_targets == 1
            else f"{record.partial_targets} targets"
            if record.time is None
            else frames_to_time_string(record.time)
        )
        if record.video_link:
            record_string = f"[{record_string}]({record.video_link})"
        players = (
            ",".join(player.name for player in record.players)
            if record.players
            else "Anonymous"
        )
        description_lines.append(
            f"{record.character.name} - {record_string} - {players}"
        )
    total_frames = sum(
        0 if (record.time is None or record.character.position > 24) else record.time
        for record in records
    )
    description_lines.append(
        f"25 Character Total: {frames_to_time_string(total_frames)}"
    )
    embed = Embed()
    embed.description = "\n".join(description_lines)
    await ctx.send(embed=embed)
    session.close()


@bot.command(aliases=["wt", "worst", "worsttotal", "wtotal"])
async def worst_total(ctx):
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.total import get_worst_total_records

    session = get_session()
    records, improvements, total = get_worst_total_records(session)
    description_lines = [
        f"{record.character.name} on {record.stage.name} ([{frames_to_time_string(record.time)}]({record.video_link}) ➛ {frames_to_time_string(improvement)})"
        for (record, improvement) in zip(records, improvements)
    ]
    description_lines.append(f"Total: {frames_to_time_string(total)}")
    embed = Embed()
    embed.description = "\n".join(description_lines)
    await ctx.send(embed=embed)
    session.close()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


bot.run(os.environ["DISCORD_TOKEN"])
