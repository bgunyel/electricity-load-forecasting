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
from backend.service.db.entities.weather_entities import WeatherStationEntity, WeatherDataEntity
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
    finally:
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
        print(f'Weather stations added to database for {code.value} - {regulator.value}')
    finally:
        session.close()


def get_stations_of_geographical_unit(
        geo_unit_code: GeographicalUnitCode,
        regulator: RegulatorType
) -> list[WeatherStationEntity]:
    g_unit = get_geographical_unit(entity_code=geo_unit_code, regulator=regulator)

    session = get_db_session(database_url=settings.DATABASE_URL)
    weather_repository = WeatherRepository(session=session)
    stations = None

    try:
        stations = weather_repository.get_weather_stations_from_geo_code_id(geo_unit_id=g_unit.id)
    except RuntimeError as e:
        print(e)
    finally:
        session.close()

    return stations


def add_new_weather_data(weather_data: list[dict], station_id: int):
    pass
    session = get_db_session(database_url=settings.DATABASE_URL)
    weather_repository = WeatherRepository(session=session)
    try:
        weather_repository.add_new_weather_data(weather_data=weather_data)
    except RuntimeError as e:
        print(e)
    finally:
        session.close()


def fetch_and_add_new_weather_data(
        geo_unit_code: GeographicalUnitCode,
        regulator: RegulatorType,
        start_date: datetime.date,
        end_date: datetime.date
):
    """
    * Get geo_unit id from geo_unit_code and regulator (via GeographicalUnitRepository)
    * Get the list of weather stations registered to the geo_unit id

    * for each station:
        * get weather data between the specified dates
        * do cleaning if there is more data than requested
        * save weather data to database with the specified station id
        * update last_valid_data_ending of the station

    """
    asos_client = ASOSClient()
    stations = get_stations_of_geographical_unit(geo_unit_code=geo_unit_code, regulator=regulator)  # active stations

    session = get_db_session(database_url=settings.DATABASE_URL)
    weather_repository = WeatherRepository(session=session)

    try:
        for station in stations:

            if end_date >= station.archive_begin:
                data_list = asos_client.get_weather_data(station_code=station.code,
                                                         start_date=max(start_date, station.archive_begin),
                                                         end_date=end_date)
                last_valid_data_ending = station.last_valid_data_ending

                if len(data_list) > 0:

                    # Updates data_list in-place (update has to be first because of 'measured_at' change)
                    _ = [
                        x.update(
                            {
                                'measured_at': datetime.datetime.fromisoformat(x['measured_at']),
                                'created_by_id': 1,
                                'updated_by_id': 1,
                                'created_at': datetime.datetime.now(datetime.timezone.utc),
                                'updated_at': datetime.datetime.now(datetime.timezone.utc),
                                'station_id': station.id,
                            }
                        ) for x in data_list
                    ]

                    if last_valid_data_ending is not None:
                        data_list = [x for x in data_list if
                                     x['measured_at'] > last_valid_data_ending]  # strict greater

                    max_data_ending = max(data_list, key=lambda x: x['measured_at'])['measured_at']

                    weather_repository.add_new_weather_data(weather_data=data_list)
                    station_update_dict = {'last_valid_data_ending': max_data_ending,
                                           'updated_at': datetime.datetime.now(datetime.timezone.utc),
                                           'updated_by_id': 1}
                    weather_repository.update_weather_station(id=station.id, update_dict=station_update_dict)

    except RuntimeError as e:
        print(e)
    finally:
        session.close()

        dummy = -32
