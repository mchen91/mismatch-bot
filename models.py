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
        try:
            alias = (
                session.query(CharacterStageAlias)
                .filter(CharacterStageAlias.name.ilike(name))
                .one()
            )
            return alias.character
        except Exception as e:
            raise ValueError(f"could not find character matching {name}")


class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    position = Column(Integer, unique=True)

    @staticmethod
    def find_by_name(name, session):
        try:
            alias = (
                session.query(CharacterStageAlias)
                .filter(CharacterStageAlias.name.ilike(name))
                .one()
            )
            return alias.stage
        except Exception as e:
            raise ValueError(f"could not find stage matching {name}")


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)

    @staticmethod
    def find_by_name(name, session):
        try:
            return session.query(Player).filter(Player.name == name).one()
        except Exception as e:
            raise ValueError(f"could not find player matching {name}")


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

    name = Column(String, index=True)
    character_id = Column(Integer, ForeignKey("character.id"))
    character = relationship("Character", backref="aliases")

    stage_id = Column(Integer, ForeignKey("stage.id"))
    stage = relationship("Stage", backref="aliases")

    @staticmethod
    def add_alias(aliased_name, known_name, session):
        character = (
            session.query(Character).filter(Character.name.ilike(known_name)).first()
        )
        stage = session.query(Stage).filter(Stage.name.ilike(known_name)).first()
        alias = CharacterStageAlias(name=aliased_name, character=character, stage=stage)
        session.add(alias)
        session.commit()
        session.close()
