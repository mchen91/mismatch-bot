from models import Player, PlayerAlias


def get_player_by_name(*, session, name):
    alias = session.query(PlayerAlias).filter(PlayerAlias.name.ilike(name)).first()
    if not alias:
        raise ValueError(f'Could not find player matching "{name}"')
    return alias.player


def create_player(*, session, name):
    from use_cases.aliases import add_player_alias

    existing_player = session.query(Player).filter(Player.name == name).first()
    if existing_player:
        raise ValueError(f'Player "{existing_player.name}" already exists')
    new_player = Player(name=name)
    session.add(new_player)
    add_player_alias(session=session, aliased_name=name, known_name=name)
    session.commit()
    return new_player
