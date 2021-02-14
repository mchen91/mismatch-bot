import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    engine = create_engine(os.environ["DATABASE_URL"])
    return sessionmaker(bind=engine)()
