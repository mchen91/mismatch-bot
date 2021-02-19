from difflib import SequenceMatcher

from models import Character, CharacterStageAlias
from use_cases.aliases import add_char_stage_alias


def get_character_by_name(*, session, name):
    all_aliases = (
        session.query(CharacterStageAlias)
        .filter(CharacterStageAlias.character != None)
        .all()
    )
    closest_alias = max(
        all_aliases,
        key=lambda alias: SequenceMatcher(
            lambda x: x in " .", alias.name.lower(), name.lower()
        ).ratio(),
    )
    return closest_alias.character


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
