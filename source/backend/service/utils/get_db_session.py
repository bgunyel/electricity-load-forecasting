from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = None


def get_db_session(database_url):
    # engine = create_engine(database_url, connect_args={'sslmode': "require"})
    global engine
    if engine is None:
        print('NEW ENGINE !')
        engine = create_engine(
            database_url,
            pool_pre_ping=True,
            pool_recycle=300,  # seconds
            echo=False,
            connect_args={
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
            }
        )
    return Session(engine)
