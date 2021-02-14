from db import get_session
from models import Character, Player, Record, Stage
from frame_conversion import time_string_to_frames

def add_record(*, character_name, stage_name, player_name=None, time_string=None, partial_targets=None, video_link=None):
    session = get_session()

    try:
        character = session.query(Character).filter(Character.name == character_name).one()
    except:
        raise ValueError(f"invalid character {character_name}")

    try:
        stage = session.query(Stage).filter(Stage.name == stage_name).one()
    except:
        raise ValueError(f"invalid stage {stage_name}")

    time_frames = None if partial_targets else time_string_to_frames(time_string)

    #TODO: check if time already exists
    record = Record(
        character=character,
        stage=stage,
        time=time_frames,
        partial_targets=partial_targets,
        video_link=video_link,
    )
    if player_name:
        try:
            player = session.query(Player).filter(Player.name == player_name).one()
        except:
            raise ValueError(f"invalid player {player_name}")
        record.players.append(player)
    session.add(record)
    session.commit()
    return record
