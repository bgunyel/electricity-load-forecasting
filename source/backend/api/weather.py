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


def fetch_weather_data(
        station_code: str,
        station_id: int,
        start_date: datetime.date,
        end_date: datetime.date
):
    asos_client = ASOSClient()
    data_list = asos_client.get_weather_data(station_code=station_code,
                                             start_date=start_date,
                                             end_date=end_date)

    if len(data_list) > 0:
        # Updates data_list in-place
        _ = [
            x.update(
                {
                    'measured_at': datetime.datetime.fromisoformat(x['measured_at']).replace(tzinfo=datetime.timezone.utc),
                    'created_by_id': 1,
                    'updated_by_id': 1,
                    'created_at': datetime.datetime.now(datetime.timezone.utc),
                    'updated_at': datetime.datetime.now(datetime.timezone.utc),
                    'station_id': station_id,
                }
            ) for x in data_list
        ]

    return data_list


def sync_weather_data_for_station(station: WeatherStationEntity):
    print(f'Station: {station.code} - {station.name}')
    MAX_QUERY_DAYS = 180
    ABSOLUTE_BEGINNING = datetime.date(year=2015, month=1, day=1)

    session = get_db_session(database_url=settings.DATABASE_URL)
    weather_repository = WeatherRepository(session=session)

    start_date = max(
        ABSOLUTE_BEGINNING if station.archive_begin is None else station.archive_begin,
        ABSOLUTE_BEGINNING if station.last_valid_data_ending is None else station.last_valid_data_ending.date()
    )
    end_date = datetime.date.today() + datetime.timedelta(days=1)  # give tomorrow's date in order to get today's data

    weather_data_list = fetch_weather_data(station_code=station.code,
                                           station_id=station.id,
                                           start_date=start_date,
                                           end_date=end_date)
    try:
        if len(weather_data_list) > 0:
            if station.last_valid_data_ending is not None:
                weather_data_list = [x for x in weather_data_list if x['measured_at'] > station.last_valid_data_ending]

            if len(weather_data_list) > 0:
                max_data_ending = max(weather_data_list, key=lambda x: x['measured_at'])['measured_at']
                weather_repository.add_new_weather_data(weather_data=weather_data_list)
                weather_repository.update_weather_station(
                    id=station.id,
                    update_dict={'last_valid_data_ending': max_data_ending,
                                 'updated_at': datetime.datetime.now(datetime.timezone.utc),
                                 'updated_by_id': 1}
                )
        """
        elif (
                (station.last_valid_data_ending is None) or
                (end_date - station.last_valid_data_ending.date() > datetime.timedelta(days=MAX_QUERY_DAYS))
        ):
            weather_repository.update_weather_station(
                id=station.id,
                update_dict={'is_active': False,
                             'updated_at': datetime.datetime.now(datetime.timezone.utc),
                             'updated_by_id': 1}
            )
        """
    except RuntimeError as e:
        print(e)
    finally:
        session.close()


def sync_weather_data(geo_unit_code: GeographicalUnitCode, regulator: RegulatorType):
    active_stations = get_stations_of_geographical_unit(geo_unit_code=geo_unit_code, regulator=regulator)

    for station in active_stations:
        sync_weather_data_for_station(station=station)
