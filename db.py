import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)


def get_session():
    return Session()
