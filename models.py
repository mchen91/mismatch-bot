from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base

import settings


Base = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))


def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)


class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True)
