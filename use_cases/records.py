from typing import List, Tuple
from sqlalchemy.orm import contains_eager
from sqlalchemy.orm.session import Session

from models import Character, Player, Record, Stage


class RecordNotBetterException(ValueError):
    pass


def add_record(
    *,
    session: Session,
    character: Character,
    stage: Stage,
    player: Player = None,
    time: int = None,
    partial_targets: int = None,
    video_link: str = None,
):
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
            elif time:
                record.partial_targets = None
                record.time = time
                record.video_link = video_link
        else:
            if record.time == time:
                record.players.append(player)
                if not record.video_link and video_link:
                    record.video_link = video_link
            elif time < record.time:
                record.time = time
                record.video_link = video_link
                record.players = [player]
            else:
                raise RecordNotBetterException
    else:
        record = Record(
            character=character,
            stage=stage,
            time=time,
            partial_targets=partial_targets,
            video_link=video_link,
        )
        if player:
            record.players.append(player)
        session.add(record)
    session.commit()
    return record


def get_record(*, session: Session, character: Character, stage: Stage):
    return (
        session.query(Record)
        .filter(
            Record.character == character,
            Record.stage == stage,
        )
        .first()
    )


def get_all_records(*, session: Session) -> List[Record]:
    return (
        session.query(Record)
        .outerjoin(Record.players)
        .options(contains_eager(Record.players))
        .all()
    )


def get_all_complete_records(*, session: Session) -> List[Record]:
    return (
        session.query(Record)
        .join(Record.players)
        .options(contains_eager(Record.players))
        .filter(Record.partial_targets == None)
        .all()
    )


def get_records_by_character(*, session: Session, character: Character) -> List[Record]:
    return (
        session.query(Record)
        .join(Stage)
        .filter(Record.character == character)
        .order_by(Stage.position)
    )


def get_records_by_stage(*, session: Session, stage: Stage) -> List[Record]:
    return (
        session.query(Record)
        .join(Character)
        .filter(Record.stage == stage)
        .order_by(Character.position)
    )


def get_fastest_stage_records(*, session: Session):
    # TODO: optimize num queries?
    records: List[Record] = []
    for stage in session.query(Stage).order_by(Stage.position):
        stage_records = session.query(Record).filter(Record.stage == stage)
        fastest_record = min(
            stage_records,
            key=lambda record: float("inf") if record.time is None else record.time,
        )
        records.append(fastest_record)
    return records


def get_formatted_record_string(*, record: Record):
    from use_cases.frame_conversion import frames_to_time_string

    return (
        f"{record.partial_targets} target"
        if record.partial_targets == 1
        else f"{record.partial_targets} targets"
        if record.time is None
        else frames_to_time_string(record.time)
    )


def get_23_stage_total(*, records: List[Record]):
    return sum(
        record.time
        for record in records
        if (
            record.time is not None
            and record.stage.position not in [17, 20]
            and 0 <= record.stage.position <= 24
        )
    )


def get_25_stage_total(*, records: List[Record]):
    return sum(
        record.time
        for record in records
        if record.time is not None and 0 <= record.stage.position <= 24
    )


def get_25_character_total(*, records: List[Record]):
    return sum(
        record.time
        for record in records
        if record.time is not None and 0 <= record.character.position <= 24
    )


def get_total(*, records: List[Record]):
    return sum(record.time for record in records if record.time is not None)


def is_vanilla_record(record: Record):
    return (
        record.character.position == record.stage.position
        and record.character.position < 25
        and record.stage.position < 25
    )


"""
SMALL NUMBER = RECORD1 WINS
1. record1 is complete, record2 is partial
    - sort ties by record2 targets
    - sort further times by record1 time
2. record1 and record2 are partial
    - sort ties by record1 targets
3. record1 and record2 are complete
    - sort ties by record1 time
4. record1 is partial, record2 is complete
    - sort ties by record1 targets
    - sort further ties by record2 time
"""


def compare_record_pair(record_pair: Tuple[Record, Record]):
    record1, record2 = record_pair
    if record1.is_complete and not record2.is_complete:
        return -1000000 * (10 - record2.partial_targets) + record1.time
    if not record1.is_complete and not record2.is_complete:
        value = 1000 * (record2.partial_targets - record1.partial_targets)
        if value == 0:
            value += record1.partial_targets
        return value
    if record1.is_complete and record2.is_complete:
        value = record1.time - record2.time
        if value == 0:
            value += record1.time / 1000.0
        return value
    if not record1.is_complete and record2.is_complete:
        return 1000000 * (10 - record1.partial_targets) - record2.time
