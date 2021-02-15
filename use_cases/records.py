from db import get_session
from models import Character, Player, Record, Stage
from frame_conversion import time_string_to_frames


def add_record(
    *,
    character_name,
    stage_name,
    player_name=None,
    time_string=None,
    partial_targets=None,
    video_link=None
):
    session = get_session()
    character = Character.find_by_name(character_name, session)
    stage = Stage.find_by_name(stage_name, session)
    player = Player.find_by_name(player_name, session) if player_name else None

    time_frames = (
        time_string_to_frames(time_string) if partial_targets is None else None
    )
    prev_records = session.query(Record).filter(
        Record.character == character,
        Record.stage == stage,
    )
    if prev_records.first():
        prev_record = prev_records.one()
        if prev_record.partial_targets is not None:
            if partial_targets:
                if partial_targets == prev_record.partial_targets:
                    if player:
                        prev_record.players.append(player)
                    if not prev_record.video_link and video_link:
                        prev_record.video_link = video_link
                elif partial_targets > prev_record.partial_targets:
                    prev_record.partial_targets = partial_targets
                    prev_record.players = [player] if player else []
                    prev_record.video_link = video_link
            elif time_frames:
                prev_record.partial_targets = None
                prev_record.time = time_frames
        else:
            if prev_record.time == time_frames:
                prev_record.players.append(player)
                if not prev_record.video_link and video_link:
                    prev_record.video_link = video_link
            elif time_frames < prev_record.time:
                prev_record.time = time_frames
                prev_record.video_link = video_link
                prev_record.players = [player]
    else:
        new_record = Record(
            character=character,
            stage=stage,
            time=time_frames,
            partial_targets=partial_targets,
            video_link=video_link,
        )
        if player:
            new_record.players.append(player)
        session.add(new_record)
    session.commit()
