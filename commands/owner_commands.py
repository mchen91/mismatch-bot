from discord.ext import commands

from db import get_session

MY_ID = 97904188918345728


def is_me():
    def predicate(ctx):
        return ctx.message.author.id == MY_ID

    return commands.check(predicate)


class OwnerCommand(commands.Cog):
    @commands.command()
    @is_me()
    async def add(
        self, ctx, character_name, stage_name, time_string, player_name, video_link
    ):
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

    @commands.command()
    @is_me()
    async def aliasc(self, ctx, aliased_name, known_name):
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
    async def aliasp(self, ctx, aliased_name, known_name):
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
