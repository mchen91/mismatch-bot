from use_cases.records import RecordNotBetterException
from discord.ext import commands
from discord.ext.commands.context import Context

from db import get_session

MY_ID = 97904188918345728


def is_me():
    def predicate(ctx: Context):
        return ctx.message.author.id == MY_ID

    return commands.check(predicate)


class OwnerCommand(commands.Cog):
    @commands.command()
    @is_me()
    async def add(
        self,
        ctx: Context,
        character_name: str,
        stage_name: str,
        time_string: str,
        player_name: str,
        video_link: str,
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
            get_23_stage_total,
            get_25_stage_total,
        )
        from use_cases.stage import get_stage_by_name

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
                    f"23 Stage total improved from {prev_23_total} to {new_23_total}"
                )
            new_frames_25_stages = get_25_stage_total(records=new_records)
            if new_frames_25_stages < prev_frames_25_stages:
                prev_25_total = frames_to_time_string(prev_frames_25_stages)
                new_25_total = frames_to_time_string(new_frames_25_stages)
                description_lines.append(
                    f"25 Stage total improved from {prev_25_total} to {new_25_total}"
                )
            # new_worst_total = get_worst_total_records(session)
            # new_best_total = get_best_total_records(session)
            # new_best_total_full_mismatch = get_best_total_full_mismatch_records(session)
            await send_embeds(description_lines, ctx)
        session.close()

    @commands.command()
    @is_me()
    async def aliasc(self, ctx: Context, aliased_name: str, known_name: str):
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

    @commands.command()
    @is_me()
    async def aliasp(self, ctx: Context, aliased_name: str, known_name: str):
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
