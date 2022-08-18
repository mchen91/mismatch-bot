from use_cases.records import RecordNotBetterException
from interactions import Client, CommandContext, Option, OptionType, Permissions

from commands.constants import GUILD_IDS  # , PERSONAL_SERVER_GUILD_ID, STADIUM_GUILD_ID
from db import get_session

MY_ID = 97904188918345728


def register_owner_commands(bot: Client):
    @bot.command(
        name="add-wr",
        description="Add a new WR",
        scope=GUILD_IDS,
        options=[
            Option(
                name="character_name",
                description="Choose a character for the WR",
                type=OptionType.STRING,
                required=True,
                # limited to 25 choices - we have 32 characters
                # choices=[create_choice(name=char, value=char) for char in CHARACTERS],
            ),
            Option(
                name="stage_name",
                description="Choose a stage for the WR",
                type=OptionType.STRING,
                required=True,
                # limited to 25 choices - we have 26 stages
                # choices=[create_choice(name=stage, value=stage) for stage in STAGES],
            ),
            Option(
                name="time_string",
                description="The record value",
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name="player_name",
                description="User who set the record",
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name="video_link",
                description="Link to the video",
                type=OptionType.STRING,
                required=True,
            ),
            Option(
                name="force",
                description="Overwrite existing record regardless of time",
                type=OptionType.BOOLEAN,
                required=False,
            ),
        ],
        default_member_permissions=Permissions.ADMINISTRATOR,
        # permissions={
        #     PERSONAL_SERVER_GUILD_ID: [
        #         create_permission(MY_ID, SlashCommandPermissionType.USER, True)
        #     ],
        #     STADIUM_GUILD_ID: [
        #         create_permission(MY_ID, SlashCommandPermissionType.USER, True)
        #     ],
        # },
        # default_permission=False,
    )
    async def _add(
        ctx: CommandContext,
        character_name: str,
        stage_name: str,
        time_string: str,
        player_name: str,
        video_link: str,
        force: bool = False,
    ):
        from use_cases.character import get_character_by_name
        from use_cases.embeds import send_embeds
        from use_cases.frame_conversion import (
            frames_to_time_string,
            time_string_to_frames,
        )
        from use_cases.player import get_player_by_name
        from use_cases.records import (
            add_record,
            get_formatted_record_string,
            get_record,
            get_records_by_character,
            get_records_by_stage,
            get_23_stage_total,
            get_25_character_total,
            get_25_stage_total,
        )
        from use_cases.stage import get_stage_by_name

        if ctx.author.id != 97904188918345728:
            return await ctx.send("get outta here")

        # from use_cases.total import get_best_total_records, get_best_total_full_mismatch_records, get_worst_total_records

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
        try:
            player = get_player_by_name(session=session, name=player_name)
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

        records = get_records_by_character(session=session, character=character)
        prev_record = get_record(session=session, character=character, stage=stage)
        prev_video_link = prev_record.video_link
        prev_record_holders = (
            ",".join(player.name for player in prev_record.players)
            if prev_record.players
            else "Anonymous"
        )
        prev_record_string = get_formatted_record_string(record=prev_record)
        prev_frames_23_stages = get_23_stage_total(records=records)
        prev_frames_25_stages = get_25_stage_total(records=records)
        prev_records_for_stage = get_records_by_stage(session=session, stage=stage)
        prev_25_char_total = get_25_character_total(records=prev_records_for_stage)
        # prev_worst_total_records = get_worst_total_records(session)
        # prev_best_total = get_best_total_records(session)
        # prev_best_total_full_mismatch = get_best_total_full_mismatch_records(session)
        try:
            record = add_record(
                session=session,
                character=character,
                stage=stage,
                player=player,
                time=time,
                partial_targets=partial_targets,
                video_link=video_link,
                force=force,
            )
        except RecordNotBetterException:
            await ctx.send(f"Did not add; worse than existing record")
        else:
            description_lines = [
                f"Improved {record.character.name}/{record.stage.name} from [{prev_record_string} by {prev_record_holders}]({prev_video_link}) to [{time_string} by {player.name}]({video_link})"
            ]
            new_records = get_records_by_character(session=session, character=character)
            new_frames_23_stages = get_23_stage_total(records=new_records)
            if new_frames_23_stages < prev_frames_23_stages:
                prev_23_total = frames_to_time_string(prev_frames_23_stages)
                new_23_total = frames_to_time_string(new_frames_23_stages)
                description_lines.append(
                    f"23 Stage total ({character.name}) improved from {prev_23_total} to {new_23_total}"
                )
            new_frames_25_stages = get_25_stage_total(records=new_records)
            if new_frames_25_stages < prev_frames_25_stages:
                prev_25_total = frames_to_time_string(prev_frames_25_stages)
                new_25_total = frames_to_time_string(new_frames_25_stages)
                description_lines.append(
                    f"25 Stage total ({character.name}) improved from {prev_25_total} to {new_25_total}"
                )
            new_stage_records = get_records_by_stage(session=session, stage=stage)
            new_stage_total = get_25_character_total(records=new_stage_records)
            if new_stage_total < prev_25_char_total:
                prev_stage_total_string = frames_to_time_string(prev_25_char_total)
                new_stage_total_string = frames_to_time_string(new_stage_total)
                description_lines.append(
                    f"25 Character total ({stage.name}) improved from {prev_stage_total_string} to {new_stage_total_string}"
                )
            # new_worst_total = get_worst_total_records(session)
            # new_best_total = get_best_total_records(session)
            # new_best_total_full_mismatch = get_best_total_full_mismatch_records(session)
            await send_embeds(description_lines, ctx)
        session.close()
