import datetime

from config import settings
from .geo_unit import add_new_geographical_unit, update_geographical_unit, get_geographical_unit
from .load_data import add_new_load_data, fetch_and_add_new_load_data, sync_load_data
from backend.service.utils.get_db_session import get_db_session

from backend.service.db.repositories.user_repository import UserRepository
from backend.service.db.repositories.geographical_unit_repository import GeographicalUnitRepository
from backend.service.db.repositories.load_data_repository import LoadDataRepository
from backend.service.db.repositories.weather_repository import WeatherRepository
from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity
from backend.service.db.models.enums import GeographicalUnitCode, GeographicalUnitType, RegulatorType

from backend.service.data_clients.entsoe import ENTSOEClient
from backend.service.data_clients.asos import ASOSClient


def fetch_and_add_weather_stations(code: GeographicalUnitCode, regulator: RegulatorType):
    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    try:
        g_unit = geographical_unit_repository.get_geographical_unit_from_code(code=code, regulator=regulator)
    except RuntimeError as e:
        print(e)
        raise RuntimeError(e)
    else:
        session.close()

    asos_client = ASOSClient()
    stations = asos_client.get_stations_for_network(country_code=code.value)

    for station in stations:
        station['geographical_unit_id'] = g_unit.id
        station['created_at'] = datetime.datetime.now(datetime.timezone.utc)
        station['updated_at'] = datetime.datetime.now(datetime.timezone.utc)
        station['created_by_id'] = 1
        station['updated_by_id'] = 1

    session = get_db_session(database_url=settings.DATABASE_URL)
    weather_repository = WeatherRepository(session=session)
    try:
        weather_repository.add_new_weather_stations(weather_stations=stations)
    except RuntimeError as e:
        print(e)
        raise RuntimeError(e)
    else:
        session.close()
