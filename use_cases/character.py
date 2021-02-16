from models import Character, CharacterStageAlias
from use_cases.aliases import add_char_stage_alias


def get_character_by_name(name, session):
    alias = (
        session.query(CharacterStageAlias)
        .filter(CharacterStageAlias.name.ilike(name))
        .first()
    )
    if not alias:
        raise ValueError(f'Could not find character matching "{name}"')
    return alias.character


def create_character(*, session, name, position):
    existing_character = session.query(Character).filter(Character.name == name).first()
    if existing_character:
        raise ValueError(f'Character "{existing_character.name}" already exists')
    new_character = Character(name=name, position=position)
    session.add(new_character)
    add_char_stage_alias(
        session=session, aliased_name=name, known_name=name, char_only=True
    )
    session.commit()
    return new_character
