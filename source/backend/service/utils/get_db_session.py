from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def get_db_session(database_url):
    engine = create_engine(database_url, connect_args={'sslmode': "require"})
    return Session(engine)
