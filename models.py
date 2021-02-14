from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    position = Column(Integer)
    records = relationship("Record", back_populates="character")


class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)
    position = Column(Integer)
    records = relationship("Record", back_populates="stage")


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)

    name = Column(String, index=True)


class Record(Base):
    __tablename__ = "record"
    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, ForeignKey("character.id"))
    character = relationship("Character", back_populates="records")

    stage_id = Column(Integer, ForeignKey("stage.id"))
    stage = relationship("Stage", back_populates="records")

    player_id = Column(Integer, ForeignKey("stage.id"), nullable=True)
    player = relationship("Player", back_populates="records")

    time = Column(Integer, index=True, nullable=True, default=None)
    partial_targets = Column(Integer, index=True, nullable=True, default=None)
    video_link = Column(String, nullable=True)

    date_created = Column(DateTime, index=True, default=datetime.now())
    date_updated = Column(
        DateTime, index=True, default=datetime.now(), onupdate=datetime.now()
    )
