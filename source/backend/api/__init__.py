from config import settings
from backend.service.utils.get_db_session import get_db_session
from backend.service.db.repositories.user_repository import UserRepository


def add_new_user(user: dict):
    session = get_db_session(database_url=settings.DATABASE_URL)
    user_repository = UserRepository(session=session)
    try:
        user_repository.insert_user(user=user)
    except RuntimeError as e:
        print(e)
    else:
        session.close()
