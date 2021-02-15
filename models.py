from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    position = Column(Integer, unique=True)

    @staticmethod
    def find_by_name(name, session):
        alias = (
            session.query(CharacterStageAlias)
            .filter(CharacterStageAlias.name.ilike(name))
            .first()
        )
        if not alias:
            raise ValueError(f"could not find character matching {name}")
        return alias.character

    @staticmethod
    def add_character(*, session, name, position):
        from use_cases.aliases import add_char_stage_alias

        existing_character = (
            session.query(Character).filter(Character.name == name).first()
        )
        if existing_character:
            raise ValueError(f"{existing_character.name} already exists")
        new_character = Character(name=name, position=position)
        session.add(new_character)
        add_char_stage_alias(
            session=session, aliased_name=name, known_name=name, char_only=True
        )
        session.commit()
        return new_character


class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    position = Column(Integer, unique=True)

    @staticmethod
    def find_by_name(name, session):
        alias = (
            session.query(CharacterStageAlias)
            .filter(CharacterStageAlias.name.ilike(name))
            .first()
        )
        if not alias:
            raise ValueError(f"could not find stage matching {name}")
        return alias.stage

    @staticmethod
    def add_stage(*, session, name, position):
        from use_cases.aliases import add_char_stage_alias

        existing_stage = session.query(Stage).filter(Stage.name == name).first()
        if existing_stage:
            raise ValueError(f"{existing_stage.name} already exists")
        new_stage = Stage(name=name, position=position)
        session.add(new_stage)
        add_char_stage_alias(
            session=session, aliased_name=name, known_name=name, stage_only=True
        )
        session.commit()
        return new_stage


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)

    @staticmethod
    def find_by_name(name, session):
        alias = session.query(PlayerAlias).filter(PlayerAlias.name.ilike(name)).first()
        if not alias:
            raise ValueError(f"could not find player matching {name}")
        return alias.player

    @staticmethod
    def add_player(*, session, name):
        from use_cases.aliases import add_player_alias

        existing_player = session.query(Player).filter(Player.name == name).first()
        if existing_player:
            raise ValueError(f"{existing_player.name} already exists")
        new_player = Player(name=name)
        session.add(new_player)
        add_player_alias(session=session, aliased_name=name, known_name=name)
        session.commit()
        return new_player


_player_record_association_table = Table(
    "record_player_association",
    Base.metadata,
    Column("player_id", Integer, ForeignKey("player.id")),
    Column("record_id", Integer, ForeignKey("record.id")),
)


class Record(Base):
    __tablename__ = "record"
    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, ForeignKey("character.id"))
    character = relationship("Character", backref="records")

    stage_id = Column(Integer, ForeignKey("stage.id"))
    stage = relationship("Stage", backref="records")

    players = relationship(
        "Player", secondary=_player_record_association_table, backref="records"
    )

    time = Column(Integer, index=True, nullable=True, default=None)
    partial_targets = Column(Integer, index=True, nullable=True, default=None)
    video_link = Column(String, nullable=True)

    date_created = Column(DateTime, index=True, default=datetime.now())
    date_updated = Column(
        DateTime, index=True, default=datetime.now(), onupdate=datetime.now()
    )


class CharacterStageAlias(Base):
    __tablename__ = "character_stage_alias"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True, unique=True)
    character_id = Column(Integer, ForeignKey("character.id"))
    character = relationship("Character", backref="aliases")

    stage_id = Column(Integer, ForeignKey("stage.id"))
    stage = relationship("Stage", backref="aliases")


class PlayerAlias(Base):
    __tablename__ = "player_alias"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True, unique=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("Player", backref="aliases")
