from models import Character, Record, Stage


def add_record(
    *,
    session,
    character,
    stage,
    player=None,
    time=None,
    partial_targets=None,
    video_link=None
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


def get_record(*, session, character, stage):
    return (
        session.query(Record)
        .filter(
            Record.character == character,
            Record.stage == stage,
        )
        .first()
    )


def get_records_by_character(*, session, character):
    return (
        session.query(Record)
        .join(Stage)
        .filter(Record.character == character)
        .order_by(Stage.position)
    )


def get_records_by_stage(*, session, stage):
    return (
        session.query(Record)
        .join(Character)
        .filter(Record.stage == stage)
        .order_by(Character.position)
    )


def get_fastest_stage_records(*, session):
    # TODO: optimize num queries?
    records = []
    for stage in session.query(Stage).order_by(Stage.position):
        stage_records = session.query(Record).filter(Record.stage == stage)
        fastest_record = min(
            stage_records,
            key=lambda record: float("inf") if record.time is None else record.time,
        )
        records.append(fastest_record)
    return records
