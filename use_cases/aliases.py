from models import Character, CharacterStageAlias, Player, PlayerAlias, Stage


def add_char_stage_alias(
    *, session, aliased_name, known_name, char_only=False, stage_only=False
):
    existing_alias = (
        session.query(CharacterStageAlias)
        .filter(CharacterStageAlias.name.ilike(aliased_name))
        .first()
    )
    existing_character = (
        session.query(Character).filter(Character.name.ilike(known_name)).first()
    )
    existing_stage = session.query(Stage).filter(Stage.name.ilike(known_name)).first()
    if existing_alias:
        if char_only and not existing_alias.character:
            existing_alias.character = existing_character
        elif stage_only and not existing_alias.stage:
            existing_alias.stage = existing_stage
        else:
            raise ValueError(f"Already aliased {aliased_name}")
        session.commit()
        return existing_alias
    character = None if stage_only else existing_character
    stage = None if char_only else existing_stage
    if not character and not stage:
        raise ValueError(f"Couldn't find character or stage matching {known_name}")
    alias = CharacterStageAlias(name=aliased_name, character=character, stage=stage)
    session.add(alias)
    session.commit()
    return alias


def add_player_alias(*, session, aliased_name, known_name):
    if session.query(PlayerAlias).filter(PlayerAlias.name.ilike(aliased_name)).first():
        raise ValueError(f"Already aliased {aliased_name}")
    player = session.query(Player).filter(Player.name.ilike(known_name)).first()
    if not player:
        raise ValueError(f"Couldn't find player matching {known_name}")
    alias = PlayerAlias(name=aliased_name, player=player)
    session.add(alias)
    session.commit()
    return alias
