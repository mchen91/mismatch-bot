from models import Character, CharacterStageAlias, Stage


def add_char_stage_alias(*, session, aliased_name, known_name):
    character = (
        session.query(Character).filter(Character.name.ilike(known_name)).first()
    )
    stage = session.query(Stage).filter(Stage.name.ilike(known_name)).first()
    alias = CharacterStageAlias(name=aliased_name, character=character, stage=stage)
    session.add(alias)
    try:
        session.commit()
    except Exception:
        raise ValueError(f"Already aliased {aliased_name}")
    return alias
