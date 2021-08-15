import os
import random
from collections import defaultdict
from decimal import Decimal

from discord.ext import commands

from commands.owner_commands import OwnerCommand
from db import get_session

COMMAND_PREFIX = "-mm "

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.command(help=f"Shows current record, e.g. {COMMAND_PREFIX}young link/samus")
async def wr(ctx, *, char_and_stage):
    from use_cases.character import get_character_by_name
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_record
    from use_cases.stage import get_stage_by_name

    combo_array = char_and_stage.split("/")
    if len(combo_array) != 2:
        await ctx.send(
            f"syntax: {COMMAND_PREFIX}<char>/<stage>. e.g. `-mm wr young link/samus`"
        )
        return
    character_name, stage_name = [s.strip() for s in combo_array]

    session = get_session()
    try:
        character = get_character_by_name(session=session, name=character_name)
    except ValueError as error:
        await ctx.send(str(error))
        return
    try:
        stage = get_stage_by_name(session=session, name=stage_name)
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


@bot.command(
    aliases=["character"],
    help=f"Shows records for a given character, e.g. {COMMAND_PREFIX}char yoshi",
)
async def char(ctx, character_name):
    from use_cases.character import get_character_by_name
    from use_cases.embeds import send_embeds
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_records_by_character

    session = get_session()
    character = get_character_by_name(session=session, name=character_name)
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
    frames_23_stages = sum(
        0
        if (
            record.time is None
            or record.stage.position in [17, 20]
            or record.stage.position > 24
        )
        else record.time
        for record in records
    )
    description_lines.append(
        f"23 Stage Total: {frames_to_time_string(frames_23_stages)}"
    )
    total_frames = sum(
        0 if (record.time is None or record.stage.position > 24) else record.time
        for record in records
    )
    description_lines.append(f"25 Stage Total: {frames_to_time_string(total_frames)}")
    await send_embeds(description_lines, ctx)
    session.close()


@bot.command(
    help=f"Shows records for a given stage, e.g. {COMMAND_PREFIX}stage mario",
)
async def stage(ctx, stage_name):
    from use_cases.embeds import send_embeds
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_records_by_stage
    from use_cases.stage import get_stage_by_name

    session = get_session()
    stage = get_stage_by_name(session=session, name=stage_name)
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
    await send_embeds(description_lines, ctx)
    session.close()


@bot.command(
    aliases=["stage-records"],
    help="Shows fastest records for each stage",
)
async def stagerecords(ctx):
    from use_cases.embeds import send_embeds
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.records import get_fastest_stage_records

    session = get_session()
    records = get_fastest_stage_records(session=session)
    description_lines = [f"Fastest Stage Records"]
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
            f"{record.character.name}/{record.stage.name} - {record_string} - {players}"
        )
    total_frames = sum(
        0 if (record.time is None or record.stage.position > 24) else record.time
        for record in records
    )
    description_lines.append(f"25 Stage Total: {frames_to_time_string(total_frames)}")
    await send_embeds(description_lines, ctx)
    session.close()


@bot.command(
    aliases=["worst", "worsttotal", "worst-total"], help="Shows worst mismatch total"
)
async def wt(ctx):
    from use_cases.embeds import send_embeds
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.total import get_worst_total_records

    session = get_session()
    records, improvements, total = get_worst_total_records(session)
    description_lines = []
    for (record, improvement) in zip(records, improvements):
        record_string = f"[{frames_to_time_string(record.time)}]({record.video_link}) ➛ {frames_to_time_string(improvement)}"
        description_lines.append(
            f"{record.character.name}/{record.stage.name} ({record_string})"
        )
    description_lines.append(f"Total: {frames_to_time_string(total)}")
    await send_embeds(description_lines, ctx)
    session.close()


@bot.command(
    aliases=["best", "besttotal", "best-total"], help="Shows best mismatch total"
)
async def bt(ctx):
    from use_cases.embeds import send_embeds
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.total import get_best_total_records

    session = get_session()
    records, total = get_best_total_records(session)
    description_lines = [
        f"{record.character.name}/{record.stage.name} - [{frames_to_time_string(record.time)}]({record.video_link}) - {','.join(player.name for player in record.players)}"
        for record in records
    ]
    description_lines.append(f"Total: {frames_to_time_string(total)}")
    await send_embeds(description_lines, ctx)
    session.close()

    session.close()


@bot.command(
    aliases=["bestfm", "besttotalfullmismatch", "bestful"],
    help="Shows best total with full mismatch (no vanilla char/stage pairings)",
)
async def btfm(ctx):
    from use_cases.embeds import send_embeds
    from use_cases.frame_conversion import frames_to_time_string
    from use_cases.total import get_best_total_full_mismatch_records

    session = get_session()
    records, total = get_best_total_full_mismatch_records(session)
    description_lines = [
        f"{record.character.name}/{record.stage.name} - [{frames_to_time_string(record.time)}]({record.video_link}) - {','.join(player.name for player in record.players)}"
        for record in records
    ]
    description_lines.append(f"Total: {frames_to_time_string(total)}")
    await send_embeds(description_lines, ctx)
    session.close()


@bot.command(aliases=["record-count"], help="Shows number of records for each player")
async def recordcount(ctx):
    from use_cases.embeds import send_embeds
    from use_cases.records import get_all_records

    session = get_session()
    records = get_all_records(session=session)
    record_count = defaultdict(int)
    for record in records:
        for player in record.players:
            record_count[player.name] += 1
    description_lines = ["Record Count"]
    for player_name, count in sorted(
        record_count.items(), key=lambda tuple: tuple[1], reverse=True
    ):
        description_lines.append(f"{player_name} - {count}")
    await send_embeds(description_lines, ctx)
    session.close()
    session.close()


### TEMP TEMP TEMP
@bot.command(aliases=["inspireme"], help="Generates a TTRC3 claim")
async def claim(ctx, char_name=None):
    from use_cases.character import get_character_by_position, get_character_by_name

    session = get_session()
    claims = [
        Decimal(str(t))
        for t in [
            7,
            9,
            8,
            10,
            7,
            10,
            10,
            10,
            6,
            7,
            3.7,
            12,
            15,
            11,
            7,
            5,
            7,
            8,
            7,
            7,
            11,
            7,
            6,
            5,
            3,
        ]
    ]
    if char_name:
        character = get_character_by_name(session=session, name=char_name)
        claim = claims[character.position]
    else:
        random_character_position = random.randint(0, 24)
        character = get_character_by_position(
            session=session, position=random_character_position
        )
        claim = claims[random_character_position]
    random_sub_amount = random.choice(
        [Decimal(str(t)) for t in [0.5, 1, 1.5, 2, 2.5, 3]]
    )
    claimed_sub = claim - random_sub_amount

    await ctx.send(f"Sub {claimed_sub} {character.name}")
    session.close()


### TEMP TEMP TEMP


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


bot.add_cog(OwnerCommand(bot))
bot.run(os.environ["DISCORD_TOKEN"])
