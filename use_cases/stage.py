from difflib import SequenceMatcher
from sqlalchemy.orm.session import Session

from models import CharacterStageAlias, Stage
from use_cases.aliases import add_char_stage_alias


def get_stage_by_name(*, session: Session, name: str):
    all_aliases = (
        session.query(CharacterStageAlias)
        .filter(CharacterStageAlias.stage != None)
        .all()
    )
    closest_alias = max(
        all_aliases,
        key=lambda alias: SequenceMatcher(
            lambda x: x in " .", alias.name.lower(), name.lower()
        ).ratio(),
    )
    return closest_alias.stage


def create_stage(*, session: Session, name: str, position: int):
    existing_stage = session.query(Stage).filter(Stage.name == name).first()
    if existing_stage:
        raise ValueError(f'Stage "{existing_stage.name}" already exists')
    new_stage = Stage(name=name, position=position)
    session.add(new_stage)
    add_char_stage_alias(
        session=session, aliased_name=name, known_name=name, stage_only=True
    )
    session.commit()
    return new_stage


def get_stage_by_position(*, session: Session, position: int):
    return session.query(Stage).filter(Stage.position == position).first()


def stages(*, session: Session):
    return session.query(Stage).order_by(Stage.position)
