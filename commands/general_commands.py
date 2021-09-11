import random
from collections import defaultdict
from decimal import Decimal
from use_cases.embeds import send_embeds

from discord.ext import commands
from discord.ext.commands.context import Context
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option

from db import get_session
from commands.constants import COMMAND_PREFIX, GUILD_IDS


class GeneralSlashCommand(commands.Cog):
    @cog_ext.cog_slash(
        name="wr",
        description="Provides the world record for a given character and stage",
        guild_ids=GUILD_IDS,
        options=[
            create_option(
                name="character",
                description="Choose a character for the WR",
                option_type=3,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            create_option(
                name="stage",
                description="Choose a stage for the WR. Defaults to the character",
                option_type=3,
                required=False,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
        ],
        connector={
            "character": "character_name",
            "stage": "stage_name",
        },
    )
    async def wr_(self, ctx: SlashContext, character_name: str, stage_name: str = None):
        from use_cases.character import get_character_by_name
        from use_cases.records import get_record, get_formatted_record_string
        from use_cases.stage import get_stage_by_name

        session = get_session()
        character = get_character_by_name(session=session, name=character_name)

        stage_name = stage_name or character_name
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
        description_lines = [f"{character.name} Character Records"]
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
                description="Order by fastest to slowest",
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
        description_lines = [f"{stage.name} Stage Records"]
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
        options=[],
    )
    async def recordcount(self, ctx: Context):
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


class GeneralCommand(commands.Cog):
    @commands.command(
        help=f"Shows current record, e.g. {COMMAND_PREFIX}wr younglink/samus"
    )
    async def wr(self, ctx: Context, char_and_stage: str):
        from use_cases.character import get_character_by_name
        from use_cases.records import get_record, get_formatted_record_string
        from use_cases.stage import get_stage_by_name

        combo_array = char_and_stage.split("/")
        if len(combo_array) != 2:
            await ctx.send(
                f"syntax: {COMMAND_PREFIX}wr <char>/<stage>. e.g. `{COMMAND_PREFIX}wr younglink/samus`"
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
            record_value = get_formatted_record_string(record=record)
            msg = f"{record.character.name}/{record.stage.name} - {record_value} by {players_string} {video_link_string}"
        else:
            msg = f"No record found for {character.name}/{stage.name}"
        await ctx.send(msg)
        session.close()

    @commands.command(
        aliases=["character"],
        help=f"Shows records for a given character, e.g. {COMMAND_PREFIX}char yoshi",
    )
    async def char(self, ctx: Context, character_name: str):
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
        description_lines = [f"{character.name} Character Records"]
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

    # TODO: refactor charsorted and stagesorted (cf. char and stage)
    @commands.command(
        aliases=[
            "charactersorted",
            "charsort",
            "charorder",
            "charordered",
            "charfast",
            "charfastest",
        ],
        help=f"Shows orderedrecords for a given character, e.g. {COMMAND_PREFIX}charsorted yoshi",
    )
    async def charsorted(self, ctx: Context, character_name: str):
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
        sorted_records = sorted(
            records,
            key=lambda record: -record.partial_targets + 1e6
            if record.time is None
            else record.time,
        )
        description_lines = [f"{character.name} Character Records"]
        for record in sorted_records:
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

    @commands.command(aliases=["chartotal"])
    async def chartotals(self, ctx: Context):
        from use_cases.character import characters
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_stage_total,
            get_records_by_character,
            get_total,
        )

        session = get_session()
        description_lines = [f"25 Stage Totals for each Character"]
        grand_total = 0
        for character in characters(session=session):
            records = get_records_by_character(session=session, character=character)
            frames_25_stages = get_25_stage_total(records=records)
            grand_total += get_total(records=records)
            description_lines.append(
                f"{character.name} - {frames_to_time_string(frames_25_stages)}"
            )
        description_lines.append(f"Grand Total: {frames_to_time_string(grand_total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    @commands.command(
        help=f"Shows records for a given stage, e.g. {COMMAND_PREFIX}stage mario",
    )
    async def stage(self, ctx: Context, stage_name: str):
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
        description_lines = [f"{stage.name} Stage Records"]
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

    @commands.command(
        aliases=[
            "stagesort",
            "stageordered",
            "stageorder",
            "stagefast",
            "stagefastest",
        ],
        help=f"Shows records for a given stage sorted from fastest to slowest, e.g. {COMMAND_PREFIX}stagesorted mario",
    )
    async def stagesorted(self, ctx: Context, stage_name: str):
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
        sorted_records = sorted(
            records,
            key=lambda record: -record.partial_targets + 1e6
            if record.time is None
            else record.time,
        )
        description_lines = [f"{stage.name} Stage Records"]
        for record in sorted_records:
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

    @commands.command(
        aliases=["stage-records"],
        help="Shows fastest records for each stage",
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

    @commands.command(aliases=["stagetotal"])
    async def stagetotals(self, ctx: Context):
        from use_cases.frame_conversion import frames_to_time_string
        from use_cases.records import (
            get_25_character_total,
            get_records_by_stage,
            get_total,
        )
        from use_cases.stage import stages

        session = get_session()
        description_lines = [f"25 Character Totals for each Stage"]
        grand_total = 0
        for stage in stages(session=session):
            records = get_records_by_stage(session=session, stage=stage)
            frames_25_stages = get_25_character_total(records=records)
            grand_total += get_total(records=records)
            description_lines.append(
                f"{stage.name} - {frames_to_time_string(frames_25_stages)}"
            )
        description_lines.append(f"Grand Total: {frames_to_time_string(grand_total)}")
        await send_embeds(description_lines, ctx)
        session.close()

    @commands.command(
        aliases=["worst", "worsttotal", "worst-total"],
        help="Shows worst mismatch total",
    )
    async def wt(self, ctx: Context):
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

    @commands.command(
        aliases=["best", "besttotal", "best-total"], help="Shows best mismatch total"
    )
    async def bt(self, ctx: Context):
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

    @commands.command(
        aliases=["bestfm", "besttotalfullmismatch", "bestful"],
        help="Shows best total with full mismatch (no vanilla char/stage pairings)",
    )
    async def btfm(self, ctx: Context):
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

    @commands.command(
        aliases=["record-count"], help="Shows number of records for each player"
    )
    async def recordcount(self, ctx: Context):
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

    @commands.command(help="Compare times between two characters")
    async def compare(self, ctx: Context, *char_names: str):
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
        characters = [
            get_character_by_name(session=session, name=char_name)
            for char_name in char_names
        ]
        records_MULTI = [
            get_records_by_character(session=session, character=character)
            for character in characters
        ]
        title = " vs. ".join(character.name for character in characters)
        description_lines = [title]
        for records in zip(*records_MULTI):
            record_string_MULTI = [
                get_formatted_record_string(record=record) for record in records
            ]
            # if record.video_link:
            #     record_string = f"[{record_string}]({record.video_link})"
            # players = (
            #     ",".join(player.name for player in record.players)
            #     if record.players
            #     else "N/A"
            # )
            joined_record_string = "/".join(record_string_MULTI)
            description_lines.append(
                f"{records[0].stage.name} - {joined_record_string}"
            )
        frames_23_stages_MULTI = [
            get_23_stage_total(records=records) for records in records_MULTI
        ]
        time_strings_23_stages_MULTI = [
            frames_to_time_string(frames) for frames in frames_23_stages_MULTI
        ]
        description_lines.append(
            f"23 Stage Total: {'/'.join(time_strings_23_stages_MULTI)}"
        )
        frames_25_stages_MULTI = [
            get_25_stage_total(records=records) for records in records_MULTI
        ]
        time_strings_25_stages_MULTI = [
            frames_to_time_string(frames) for frames in frames_25_stages_MULTI
        ]
        description_lines.append(
            f"25 Stage Total: {'/'.join(time_strings_25_stages_MULTI)}"
        )
        await send_embeds(description_lines, ctx)
        session.close()

    @commands.command(name="random")
    async def random_(self, ctx: Context):
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

    @commands.command(name="primes")
    async def primes_(self, ctx: Context):
        from use_cases.primes import is_prime
        from use_cases.records import get_all_complete_records

        session = get_session()
        complete_records = get_all_complete_records(session=session)
        num_prime_framed_records = sum(
            1 for record in complete_records if is_prime(record.time)
        )
        msg = f"There are {num_prime_framed_records} records with a prime frame count"
        await ctx.send(msg)
        session.close()

    ### TEMP TEMP TEMP
    @commands.command(aliases=["inspireme"], help="Generates a TTRC3 claim")
    async def claim(self, ctx: Context, char_name: str = None):
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
