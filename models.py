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


class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    position = Column(Integer, unique=True)


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)


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
