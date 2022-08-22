import random
from decimal import Decimal
from collections import defaultdict
from typing import Optional
from use_cases.embeds import send_embeds
from interactions import Choice, Client, CommandContext, Option, OptionType

from db import get_session
from commands.constants import GUILD_IDS


def register_general_commands(bot: Client):
    @bot.command(
        name="wr",
        description="Provides the world record for a given character and stage",
        scope=GUILD_IDS,
        options=[
            Option(
                name="character",
                description="Choose a character for the WR",
                type=OptionType.STRING,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            Option(
                name="stage",
                description="Choose a stage for the WR",
                type=OptionType.STRING,
                required=True,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
    )
    async def _wr(ctx: CommandContext, **kwargs):
        character_name: str = kwargs["character"]
        stage_name: str = kwargs["stage"]
        from use_cases.character import get_character_by_name
        from use_cases.records import get_record, get_formatted_record_string
        from use_cases.stage import get_stage_by_name

        session = get_session()
        character = get_character_by_name(session=session, name=character_name)

        stage = get_stage_by_name(session=session, name=stage_name)
        record = get_record(session=session, character=character, stage=stage)

        if record:
            players_string = (
                ",".join(player.name for player in record.players) or "Anonymous"
            )
            video_link_string = f"at {record.video_link}" if record.video_link else ""
            record_value = get_formatted_record_string(record=record)
            msg = f"{record.character.name}/{record.stage.name} - {record_value} by {players_string} {video_link_string}"
        else:
            msg = f"No record found for {character.name}/{stage.name}"
        await ctx.send(msg)
        session.close()

    @bot.command(
        name="char",
        description="Shows records for a given character",
        scope=GUILD_IDS,
        options=[
            Option(
                name="character",
                description="Choose a character",
                type=OptionType.STRING,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            Option(
                name="sorted",
                description="Order by fastest to slowest",
                type=OptionType.BOOLEAN,
                required=False,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
    )
    async def _char(ctx: CommandContext, **kwargs):
        from use_cases.character import get_character_by_name
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_23_stage_total,
            get_25_stage_total,
            get_formatted_record_string,
            get_records_by_character,
        )

        character_name: str = kwargs["character"]
        is_sorted: bool = kwargs.get("sorted", False)
        session = get_session()
        character = get_character_by_name(session=session, name=character_name)
        records = get_records_by_character(session=session, character=character)
        description_lines = [
            f"{character.name} Character Records{' (sorted)' if is_sorted else ''}"
        ]
        if is_sorted:
            records = sorted(
                records,
                key=lambda record: -record.partial_targets + 1e6
                if record.time is None
                else record.time,
            )
        for record in records:
            record_string = get_formatted_record_string(record=record)
            if record.video_link:
                record_string = f"[{record_string}]({record.video_link})"
            players = (
                ",".join(player.name for player in record.players)
                if record.players
                else "N/A"
            )
            description_lines.append(
                f"{record.stage.name} - {record_string} - {players}"
            )
        frames_23_stages = get_23_stage_total(records=records)
        description_lines.append(
            f"23 Stage Total: {frames_to_time_string(frames_23_stages)}"
        )
        total_frames = get_25_stage_total(records=records)
        description_lines.append(
            f"25 Stage Total: {frames_to_time_string(total_frames)}"
        )
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="stage",
        description="Shows records for a given stage",
        scope=GUILD_IDS,
        options=[
            Option(
                name="stage",
                description="Choose a stage",
                type=OptionType.STRING,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            Option(
                name="sorted",
                description="Order by fastest to slowest (default: False)",
                type=OptionType.BOOLEAN,
                required=False,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
    )
    async def _stage(ctx: CommandContext, **kwargs):
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_character_total,
            get_formatted_record_string,
            get_records_by_stage,
        )
        from use_cases.stage import get_stage_by_name

        stage_name: str = kwargs["stage"]
        is_sorted: bool = kwargs.get("sorted", False)
        session = get_session()
        stage = get_stage_by_name(session=session, name=stage_name)
        records = get_records_by_stage(session=session, stage=stage)
        if is_sorted:
            records = sorted(
                records,
                key=lambda record: -record.partial_targets + 1e6
                if record.time is None
                else record.time,
            )
        description_lines = [
            f"{stage.name} Stage Records{' (sorted)' if is_sorted else ''}"
        ]
        for record in records:
            record_string = get_formatted_record_string(record=record)
            if record.video_link:
                record_string = f"[{record_string}]({record.video_link})"
            players = (
                ",".join(player.name for player in record.players)
                if record.players
                else "N/A"
            )
            description_lines.append(
                f"{record.character.name} - {record_string} - {players}"
            )
        total_frames = get_25_character_total(records=records)
        description_lines.append(
            f"25 Character Total: {frames_to_time_string(total_frames)}"
        )
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="recordcount",
        description="Displays the record count for each player",
        scope=GUILD_IDS,
        options=[
            Option(
                name="mode",
                description="Optionally choose between mismatch only, vanilla only, or all records (default: all)",
                type=OptionType.STRING,
                choices=[
                    Choice(
                        name="All (default)",
                        value="all",
                    ),
                    Choice(
                        name="Mismatch only",
                        value="mismatch-only",
                    ),
                    Choice(
                        name="Vanilla only",
                        value="vanilla-only",
                    ),
                ],
                required=False,
            ),
        ],
    )
    async def _recordcount(ctx: CommandContext, mode: str = "all"):
        from use_cases.embeds import send_embeds
        from use_cases.records import get_all_records, is_vanilla_record

        session = get_session()
        records = get_all_records(session=session)
        record_count = defaultdict(int)
        for record in records:
            is_vanilla = is_vanilla_record(record)
            if mode == "mismatch-only" and is_vanilla:
                continue
            if mode == "vanilla-only" and not is_vanilla:
                continue
            for player in record.players:
                record_count[player.name] += 1
        title = "Record Count"
        if mode == "mismatch-only":
            title = "Record Count (Mismatch only)"
        elif mode == "vanilla-only":
            title = "Record Count (Vanilla only)"
        description_lines = [title]
        for player_name, count in sorted(
            record_count.items(), key=lambda tuple: tuple[1], reverse=True
        ):
            description_lines.append(f"{player_name} - {count}")
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="primes",
        description="Displays the number of records with a prime frame count or targets completed",
        scope=GUILD_IDS,
    )
    async def primes(ctx: CommandContext):
        from use_cases.primes import is_prime
        from use_cases.records import get_all_records

        session = get_session()
        num_prime_framed_records = num_prime_framed_target_hits = 0
        for record in get_all_records(session=session):
            if record.time:
                if is_prime(record.time):
                    num_prime_framed_records += 1
            else:
                if is_prime(record.partial_targets):
                    num_prime_framed_target_hits += 1
        msg_lines = [
            f"There are {num_prime_framed_records} records with a prime frame count",
            f"There are {num_prime_framed_target_hits} records with a prime number of targets hit",
        ]

        await ctx.send("\n".join(msg_lines))
        session.close()

    @bot.command(
        name="compare",
        description="Compare times between two characters",
        scope=GUILD_IDS,
        options=[
            Option(
                name="character1",
                description="First character to compare",
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name="character2",
                description="Second character to compare",
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name="sort_by",
                description="Optionally choose how to sort the results",
                type=OptionType.STRING,
                choices=[
                    Choice(
                        name="Stage (default)",
                        value="stage",
                    ),
                    Choice(
                        name="Delta",
                        value="delta",
                    ),
                ],
                required=False,
            ),
        ],
    )
    async def _compare(
        ctx: CommandContext, character1: str, character2: str, sort_by: str = "stage"
    ):
        from use_cases.character import get_character_by_name
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            compare_record_pair,
            get_23_stage_total,
            get_25_stage_total,
            get_common_stage_totals,
            get_formatted_record_string,
            get_records_by_character,
        )

        char_names = [character1, character2]

        session = get_session()
        characters = [
            get_character_by_name(session=session, name=char_name)
            for char_name in char_names
        ]
        records_MULTI = [
            get_records_by_character(session=session, character=character)
            for character in characters
        ]
        records_zipped = zip(*records_MULTI)
        if sort_by == "delta":
            records_zipped = sorted(
                records_zipped,
                key=compare_record_pair,
            )
        title_vs = " vs. ".join(character.name for character in characters)
        title_sort = " (sorted by Delta)" if sort_by == "delta" else ""
        title = f"{title_vs}{title_sort}"
        description_lines = [title]
        for records in records_zipped:
            record_string_MULTI = [
                get_formatted_record_string(record=record) for record in records
            ]
            # record_string_MULTI: ["9.90", "9.97"]
            record_string_with_video_MULTI = [
                f"[{record_string}]({record.video_link})"
                if record.video_link
                else record_string
                for (record, record_string) in zip(records, record_string_MULTI)
            ]
            # record_string_with_video_MULTI: ["[9.90"]
            joined_record_string = " vs. ".join(record_string_with_video_MULTI)
            delta = (
                f" ({records[0].time - records[1].time} frames)"
                if records[0].is_complete and records[1].is_complete
                else ""
            )
            description_lines.append(
                f"{records[0].stage.name} - {joined_record_string}{delta}"
            )
        frames_23_stages_MULTI = [
            get_23_stage_total(records=records) for records in records_MULTI
        ]
        time_strings_23_stages_MULTI = [
            frames_to_time_string(frames) for frames in frames_23_stages_MULTI
        ]
        description_lines.append(
            f"23 Stage Total: {' vs. '.join(time_strings_23_stages_MULTI)}"
        )
        frames_25_stages_MULTI = [
            get_25_stage_total(records=records) for records in records_MULTI
        ]
        time_strings_25_stages_MULTI = [
            frames_to_time_string(frames) for frames in frames_25_stages_MULTI
        ]
        description_lines.append(
            f"25 Stage Total: {' vs. '.join(time_strings_25_stages_MULTI)}"
        )
        (frames_common_stages_MULTI, num_common_stages) = get_common_stage_totals(
            record_lists=records_MULTI
        )
        time_strings_common_stages_MULTI = [
            frames_to_time_string(frames) for frames in frames_common_stages_MULTI
        ]
        description_lines.append(
            f"Common ({num_common_stages}) Stage Total: {' vs. '.join(time_strings_common_stages_MULTI)}"
        )
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="random",
        description="Displays a random mismatch record",
        scope=GUILD_IDS,
        options=[
            Option(
                name="character",
                description="Choose a character (optional)",
                type=OptionType.STRING,
                required=False,
            ),
            Option(
                name="stage",
                description="Choose a stage (optional)",
                type=OptionType.STRING,
                required=False,
            ),
            Option(
                name="player",
                description="Choose a player (optional)",
                type=OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def _random(ctx: CommandContext, character=None, stage=None, player=None):
        from use_cases.character import get_character_by_name
        from use_cases.stage import get_stage_by_name
        from use_cases.player import guess_player_by_name
        from use_cases.records import (
            get_complete_records,
            get_formatted_record_string,
        )

        session = get_session()
        if character:
            character = get_character_by_name(session=session, name=character)
        if stage:
            stage = get_stage_by_name(session=session, name=stage)
        if player:
            player = guess_player_by_name(session=session, name=player)
        complete_records = get_complete_records(
            session=session, character=character, stage=stage, player=player
        )
        try:
            record = random.choice(complete_records)
        except IndexError:
            msg = f"No records found for player {player.name}"
        else:
            players_string = ",".join(player.name for player in record.players)
            record_value = get_formatted_record_string(record=record)
            video_link_string = f"at {record.video_link}"
            msg = f"{record.character.name}/{record.stage.name} - {record_value} by {players_string} {video_link_string}"
        await ctx.send(msg)
        session.close()

    @bot.command(
        name="claim",
        description="Displays a random TTRC5 claim",
        scope=GUILD_IDS,
        options=[
            Option(
                name="character",
                description="Optionally select a character",
                type=OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def _claim(ctx: CommandContext, **kwargs):
        from use_cases.character import get_character_by_position, get_character_by_name

        character_name: Optional[str] = kwargs.get("character", None)
        session = get_session()
        claims = [
            Decimal(str(t))
            for t in [
                10,
                9,
                3.5,
                5.5,
                6.93,
                7.82,
                6.70,
                9.5,
                9.8,
                4.87,
                7.5,
                12.5,
                6.66,
                6.70,
                3.7,
                10,
                7,
                8,
                7.5,
                7.23,
                3.9,
                8.78,
                9.20,
                9,
                9.95,
            ]
        ]
        if character_name:
            character = get_character_by_name(session=session, name=character_name)
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

    @bot.command(
        name="wt",
        description="Displays the assignment of characters to stages that results in the worst total",
        scope=GUILD_IDS,
    )
    async def _wt(ctx: CommandContext):
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.total import get_worst_total_records

        session = get_session()
        records, improvements, total = get_worst_total_records(session)
        description_lines = ["Worst Total"]
        for (record, improvement) in zip(records, improvements):
            record_string = f"[{frames_to_time_string(record.time)}]({record.video_link}) ➛ {frames_to_time_string(improvement)}"
            description_lines.append(
                f"{record.character.name}/{record.stage.name} ({record_string})"
            )
        description_lines.append(f"Total: {frames_to_time_string(total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="bt",
        description="Displays the assignment of characters to stages that results in the best total",
        scope=GUILD_IDS,
        options=[
            Option(
                name="allow_vanilla",
                description="Allow vanilla pairings (default: False)",
                type=OptionType.BOOLEAN,
                required=False,
            ),
        ],
    )
    async def _bt(ctx: CommandContext, allow_vanilla: bool = False):
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.total import (
            get_best_total_full_mismatch_records,
            get_best_total_records,
        )

        session = get_session()
        records, total = (
            get_best_total_records(session)
            if allow_vanilla
            else get_best_total_full_mismatch_records(session)
        )
        description_lines = [
            "Best Total (Allowing Vanilla Pairings)"
            if allow_vanilla
            else "Best Total (Full Mismatch)"
        ]
        description_lines += [
            f"{record.character.name}/{record.stage.name} - [{frames_to_time_string(record.time)}]({record.video_link}) - {','.join(player.name for player in record.players)}"
            for record in records
        ]
        description_lines.append(f"Total: {frames_to_time_string(total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="stagerecords",
        description="Displays the fastest records for each stage",
        scope=GUILD_IDS,
    )
    async def _stagerecords(ctx: CommandContext):
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_stage_total,
            get_fastest_stage_records,
            get_formatted_record_string,
        )

        session = get_session()
        records = get_fastest_stage_records(session=session)
        description_lines = [f"Fastest Stage Records"]
        for record in records:
            record_string = get_formatted_record_string(record=record)
            if record.video_link:
                record_string = f"[{record_string}]({record.video_link})"
            players = (
                ",".join(player.name for player in record.players)
                if record.players
                else "N/A"
            )
            description_lines.append(
                f"{record.character.name}/{record.stage.name} - {record_string} - {players}"
            )
        total_frames = get_25_stage_total(records=records)
        description_lines.append(
            f"25 Stage Total: {frames_to_time_string(total_frames)}"
        )
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="totals",
        description="List either char or stage totals",
        scope=GUILD_IDS,
        options=[
            Option(
                name="mode",
                description="Choose between totals for each character or for each stage",
                type=OptionType.STRING,
                required=True,
                choices=[
                    Choice(
                        name="character totals (25 stage)",
                        value="character25",
                    ),
                    Choice(
                        name="character totals (23 stage)",
                        value="character23",
                    ),
                    Choice(
                        name="stage totals",
                        value="stage",
                    ),
                ],
            ),
            Option(
                name="sorted",
                description="Order by fastest to slowest (default: False)",
                type=OptionType.BOOLEAN,
                required=False,
            ),
        ],
    )
    async def _totals(ctx: CommandContext, mode: str, **kwargs):
        is_sorted = kwargs.get("sorted", False)
        if mode == "character25":
            await _chartotals25(ctx, is_sorted)
        if mode == "character23":
            await _chartotals23(ctx, is_sorted)
        elif mode == "stage":
            await _stagetotals(ctx, is_sorted)

    async def _chartotals25(ctx: CommandContext, is_sorted: bool):
        from use_cases.character import characters
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_stage_total,
            get_records_by_character,
            get_total,
        )

        session = get_session()
        description_lines = [
            f"25 Stage Totals for each Character{' (sorted)' if is_sorted else ''}"
        ]
        total_25x25 = 0
        grand_total = 0
        char_to_total_tuples = []
        for character in characters(session=session):
            records = get_records_by_character(session=session, character=character)
            frames_25_stages = get_25_stage_total(records=records)
            char_to_total_tuples.append((character, frames_25_stages))
            if character.position < 25:
                total_25x25 += frames_25_stages
            grand_total += get_total(records=records)
        if is_sorted:
            char_to_total_tuples = sorted(
                char_to_total_tuples,
                key=lambda tup: tup[1],
            )
        for character, total in char_to_total_tuples:
            description_lines.append(
                f"{character.name} - {frames_to_time_string(total)}"
            )
        description_lines.append(f"25x25 Total: {frames_to_time_string(total_25x25)}")
        description_lines.append(f"Grand Total: {frames_to_time_string(grand_total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    async def _chartotals23(ctx: CommandContext, is_sorted: bool):
        from use_cases.character import characters
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_23_stage_total,
            get_records_by_character,
            get_total,
        )

        session = get_session()
        description_lines = [
            f"23 Stage Totals for each Character{' (sorted)' if is_sorted else ''}"
        ]
        grand_total = 0
        char_to_total_tuples = []
        for character in characters(session=session):
            records = get_records_by_character(session=session, character=character)
            records_23 = [
                record for record in records if record.stage.position not in [17, 20]
            ]
            frames_23_stages = get_23_stage_total(records=records_23)
            char_to_total_tuples.append((character, frames_23_stages))
            grand_total += get_total(records=records_23)
        if is_sorted:
            char_to_total_tuples = sorted(
                char_to_total_tuples,
                key=lambda tup: tup[1],
            )
        for character, total in char_to_total_tuples:
            description_lines.append(
                f"{character.name} - {frames_to_time_string(total)}"
            )
        description_lines.append(f"Grand Total: {frames_to_time_string(grand_total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    async def _stagetotals(ctx: CommandContext, is_sorted: bool):
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_character_total,
            get_records_by_stage,
            get_total,
        )
        from use_cases.stage import stages

        session = get_session()
        description_lines = [
            f"25 Character Totals for each Stage{' (sorted)' if is_sorted else ''}"
        ]
        grand_total = 0
        stage_to_total_tuples = []
        for stage in stages(session=session):
            records = get_records_by_stage(session=session, stage=stage)
            frames_25_stages = get_25_character_total(records=records)
            stage_to_total_tuples.append((stage, frames_25_stages))
            grand_total += get_total(records=records)

        if is_sorted:
            stage_to_total_tuples = sorted(
                stage_to_total_tuples,
                key=lambda tup: tup[1],
            )
        for stage, frames_25_stages in stage_to_total_tuples:
            description_lines.append(
                f"{stage.name} - {frames_to_time_string(frames_25_stages)}"
            )
        description_lines.append(f"Grand Total: {frames_to_time_string(grand_total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    @bot.command(
        name="randtotal",
        description="Displays a randomly assigned mismatch total",
        scope=GUILD_IDS,
        options=[
            Option(
                name="allow_vanilla",
                description="Allow vanilla pairings (default: False)",
                type=OptionType.BOOLEAN,
                required=False,
            ),
        ],
    )
    async def _rand_total(ctx: CommandContext, allow_vanilla: bool = False):
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.total import get_random_total

        session = get_session()
        records, total = get_random_total(session=session, allow_vanilla=allow_vanilla)
        description_lines = [
            "Random Total (Allowing Vanilla Pairings)"
            if allow_vanilla
            else "Random Total (Full Mismatch)"
        ]
        description_lines += [
            f"{record.character.name}/{record.stage.name} - [{frames_to_time_string(record.time)}]({record.video_link}) - {','.join(player.name for player in record.players)}"
            for record in records
        ]
        description_lines.append(f"Total: {frames_to_time_string(total)}")
        await send_embeds(description_lines, ctx)
        session.close()
