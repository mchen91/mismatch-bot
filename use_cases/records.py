from models import Record
from use_cases.character import get_character_by_name
from use_cases.frame_conversion import time_string_to_frames
from use_cases.player import get_player_by_name
from use_cases.stage import get_stage_by_name


def add_record(
    *,
    session,
    character_name,
    stage_name,
    player_name=None,
    time_string=None,
    partial_targets=None,
    video_link=None
):
    character = get_character_by_name(character_name, session)
    stage = get_stage_by_name(stage_name, session)
    player = get_player_by_name(player_name, session) if player_name else None

    time_frames = (
        time_string_to_frames(time_string) if partial_targets is None else None
    )
    prev_records = session.query(Record).filter(
        Record.character == character,
        Record.stage == stage,
    )
    if prev_records.first():
        record = prev_records.one()
        if record.partial_targets is not None:
            if partial_targets:
                if partial_targets == record.partial_targets:
                    if player:
                        record.players.append(player)
                    if not record.video_link and video_link:
                        record.video_link = video_link
                elif partial_targets > record.partial_targets:
                    record.partial_targets = partial_targets
                    record.players = [player] if player else []
                    record.video_link = video_link
            elif time_frames:
                record.partial_targets = None
                record.time = time_frames
        else:
            if record.time == time_frames:
                record.players.append(player)
                if not record.video_link and video_link:
                    record.video_link = video_link
            elif time_frames < record.time:
                record.time = time_frames
                record.video_link = video_link
                record.players = [player]
    else:
        record = Record(
            character=character,
            stage=stage,
            time=time_frames,
            partial_targets=partial_targets,
            video_link=video_link,
        )
        if player:
            record.players.append(player)
        session.add(record)
    session.commit()
    return record


def get_record(*, session, character, stage):
    return (
        session.query(Record)
        .filter(
            Record.character == character,
            Record.stage == stage,
        )
        .first()
    )
