import random
from collections import defaultdict
from use_cases.embeds import send_embeds

from discord.ext import commands
from discord.ext.commands.context import Context
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from db import get_session
from commands.constants import GUILD_IDS


class GeneralSlashCommand(commands.Cog):
    @cog_ext.cog_slash(
        name="wr",
        description="Provides the world record for a given character and stage",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="character",
                description="Choose a character for the WR",
                option_type=str,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            create_option(
                name="stage",
                description="Choose a stage for the WR",
                option_type=str,
                required=True,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
        connector={
            "character": "character_name",
            "stage": "stage_name",
        },
    )
    async def wr(self, ctx: SlashContext, character_name: str, stage_name: str):
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

    @cog_ext.cog_slash(
        name="char",
        description="Shows records for a given character",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="character",
                description="Choose a character",
                option_type=3,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            create_option(
                name="sorted",
                description="Order by fastest to slowest",
                option_type=5,
                required=False,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
        connector={
            "character": "character_name",
            "sorted": "is_sorted",
        },
    )
    async def char(self, ctx: Context, character_name: str, is_sorted: bool = False):
        from use_cases.character import get_character_by_name
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_23_stage_total,
            get_25_stage_total,
            get_formatted_record_string,
            get_records_by_character,
        )

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

    @cog_ext.cog_slash(
        name="stage",
        description="Shows records for a given stage",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="stage",
                description="Choose a stage",
                option_type=3,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            create_option(
                name="sorted",
                description="Order by fastest to slowest (default: False)",
                option_type=5,
                required=False,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
        connector={
            "stage": "stage_name",
            "sorted": "is_sorted",
        },
    )
    async def stage(self, ctx: Context, stage_name: str, is_sorted: bool = False):
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_character_total,
            get_formatted_record_string,
            get_records_by_stage,
        )
        from use_cases.stage import get_stage_by_name

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

    @cog_ext.cog_slash(
        name="recordcount",
        description="Displays the record count for each player",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="mode",
                description="Optionally choose between mismatch only, vanilla only, or all records (default: all)",
                option_type=3,
                choices=[
                    create_choice(
                        name="All (default)",
                        value="all",
                    ),
                    create_choice(
                        name="Mismatch only",
                        value="mismatch-only",
                    ),
                    create_choice(
                        name="Vanilla only",
                        value="vanilla-only",
                    ),
                ],
                required=False,
            ),
        ],
    )
    async def recordcount(self, ctx: Context, mode: str = "all"):
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

    @cog_ext.cog_slash(
        name="primes",
        description="Displays the number of records with a prime frame count or targets completed",
        guild_ids=GUILD_IDS,
    )
    async def primes(self, ctx: Context):
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

    @cog_ext.cog_slash(
        name="compare",
        description="Compare times between two characters",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="character1",
                description="First character to compare",
                option_type=str,
                required=True,
            ),
            create_option(
                name="character2",
                description="Second character to compare",
                option_type=3,
                required=True,
            ),
            create_option(
                name="sort_by",
                description="Optionally choose how to sort the results",
                option_type=str,
                choices=[
                    create_choice(
                        name="Stage (default)",
                        value="stage",
                    ),
                    create_choice(
                        name="Delta",
                        value="delta",
                    ),
                ],
                required=False,
            ),
        ],
    )
    async def compare(
        self, ctx: Context, character1: str, character2: str, sort_by: str = "stage"
    ):
        from use_cases.character import get_character_by_name
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            compare_record_pair,
            get_23_stage_total,
            get_25_stage_total,
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
        await send_embeds(description_lines, ctx)
        session.close()

    @cog_ext.cog_slash(
        name="random",
        description="Displays a random mismatch record",
        guild_ids=GUILD_IDS,
    )
    async def random(self, ctx: Context):
        from use_cases.records import (
            get_all_complete_records,
            get_formatted_record_string,
        )

        session = get_session()
        complete_records = get_all_complete_records(session=session)
        record = random.choice(complete_records)
        players_string = ",".join(player.name for player in record.players)
        record_value = get_formatted_record_string(record=record)
        video_link_string = f"at {record.video_link}"
        msg = f"{record.character.name}/{record.stage.name} - {record_value} by {players_string} {video_link_string}"
        await ctx.send(msg)
        session.close()

    @cog_ext.cog_slash(
        name="wt",
        description="Displays the assignment of characters to stages that results in the worst total",
        guild_ids=GUILD_IDS,
    )
    async def wt(self, ctx: Context):
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

    @cog_ext.cog_slash(
        name="bt",
        description="Displays the assignment of characters to stages that results in the best total",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="allow_vanilla",
                description="Allow vanilla pairings (default: False)",
                option_type=5,
                required=False,
            ),
        ],
    )
    async def bt(self, ctx: Context, allow_vanilla: bool = False):
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

    @cog_ext.cog_slash(
        name="stagerecords",
        description="Displays the fastest records for each stage",
        guild_ids=GUILD_IDS,
    )
    async def stagerecords(self, ctx: Context):
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

    @cog_ext.cog_slash(
        name="totals",
        description="List either char or stage totals",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="mode",
                description="Choose between totals for each character or for each stage",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="character totals",
                        value="character",
                    ),
                    create_choice(
                        name="stage totals",
                        value="stage",
                    ),
                ],
            ),
            create_option(
                name="sorted",
                description="Order by fastest to slowest (default: False)",
                option_type=5,
                required=False,
            ),
        ],
        connector={
            "sorted": "is_sorted",
        },
    )
    async def totals(self, ctx: Context, mode: str, is_sorted: bool = False):
        if mode == "character":
            await self._chartotals(ctx, is_sorted)
        elif mode == "stage":
            await self._stagetotals(ctx, is_sorted)

    async def _chartotals(self, ctx: Context, is_sorted: bool):
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
        grand_total = 0
        char_to_total_tuples = []
        for character in characters(session=session):
            records = get_records_by_character(session=session, character=character)
            frames_25_stages = get_25_stage_total(records=records)
            char_to_total_tuples.append((character, frames_25_stages))
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
        description_lines.append(f"Grand Total: {frames_to_time_string(grand_total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    async def _stagetotals(self, ctx: Context, is_sorted: bool):
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
