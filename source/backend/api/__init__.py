from config import settings
from backend.service.utils.get_db_session import get_db_session
from backend.service.db.repositories.user_repository import UserRepository
from backend.service.db.repositories.geographical_unit_repository import GeographicalUnitRepository

from backend.service.db.models.enums import GeographicalUnitCode, GeographicalUnitType, RegulatorType


def add_new_user(user: dict):
    session = get_db_session(database_url=settings.DATABASE_URL)
    user_repository = UserRepository(session=session)
    try:
        user_repository.insert_user(user=user)
    except RuntimeError as e:
        print(e)
    else:
        session.close()


def add_new_geographical_unit(geographical_unit: dict):
    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    try:
        geographical_unit_repository.add_new_geographical_unit(geographical_unit=geographical_unit)
    except RuntimeError as e:
        print(e)
    else:
        session.close()


__all__ = [
    'GeographicalUnitCode',
    'GeographicalUnitType',
    'RegulatorType',
    'add_new_user',
    'add_new_geographical_unit',
]
