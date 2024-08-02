from backend.service.db.models.enums import GeographicalUnitCode, GeographicalUnitType, RegulatorType
from backend.service.db.repositories.geographical_unit_repository import GeographicalUnitRepository
from backend.service.db.repositories.user_repository import UserRepository
from backend.service.utils.get_db_session import get_db_session
from config import settings
from .geo_unit import add_new_geographical_unit, update_geographical_unit, get_geographical_unit
from .load_data import add_new_load_data, fetch_and_add_new_load_data, sync_load_data
from .weather import fetch_and_add_weather_stations


def add_new_user(user: dict):
    session = get_db_session(database_url=settings.DATABASE_URL)
    user_repository = UserRepository(session=session)
    try:
        user_repository.insert_user(user=user)
    except RuntimeError as e:
        print(e)
    else:
        session.close()


def sync_all_data():
    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    geographical_units = None

    try:
        geographical_units = (
            geographical_unit_repository.get_geographical_units_of_regulator(regulator=RegulatorType.ENTSOE)
        )
    except RuntimeError as e:
        print(e)
    else:
        session.close()

    for g_unit in geographical_units:
        print(f'Syncing: {g_unit.name} - {g_unit.code.value}')
        sync_load_data(entity_code=g_unit.code, regulator=RegulatorType.ENTSOE)


################
# API Exposure #
################
__all__ = [
    'GeographicalUnitCode',
    'GeographicalUnitType',
    'RegulatorType',
    'add_new_user',
    'add_new_geographical_unit',
    'add_new_load_data',
    'fetch_and_add_new_load_data',
    'fetch_and_add_weather_stations',
    'update_geographical_unit',
    'sync_load_data',
    'sync_all_data',
]
