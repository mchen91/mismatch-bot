import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


engine = create_engine(os.environ["DATABASE_URL"])
SessionFactory = sessionmaker(bind=engine)


def get_session() -> Session:
    return SessionFactory()
