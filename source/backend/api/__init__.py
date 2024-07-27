import datetime

from config import settings
from backend.service.utils.get_db_session import get_db_session
from backend.service.db.repositories.user_repository import UserRepository
from backend.service.db.repositories.geographical_unit_repository import GeographicalUnitRepository
from backend.service.db.repositories.load_data_repository import LoadDataRepository
from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity
from backend.service.db.models.enums import GeographicalUnitCode, GeographicalUnitType, RegulatorType

from backend.service.data_clients.entsoe import ENTSOEClient


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
    """
    geographical_unit = {
        'code': GeographicalUnitCode.TURKIYE,
        'name': 'Turkiye',
        'type': GeographicalUnitType.COUNTRY,
        'regulator': RegulatorType.EPIAS,
        'is_active': True,
        'created_by_id': 1,
        'updated_by_id': 1,
        'created_at': datetime.datetime.now(datetime.timezone.utc),
        'updated_at': datetime.datetime.now(datetime.timezone.utc),
    }
    """

    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    try:
        geographical_unit_repository.add_new_geographical_unit(geographical_unit=geographical_unit)
    except RuntimeError as e:
        print(e)
    else:
        session.close()


def update_geographical_unit(
        code: GeographicalUnitCode,
        regulator: RegulatorType,
        last_valid_data_ending: datetime.datetime
):
    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    try:
        geographical_unit_repository.update_geographical_unit(code=code, regulator=regulator,
                                                              last_valid_data_ending=last_valid_data_ending)
    except RuntimeError as e:
        print(e)
    else:
        session.close()


def add_new_load_data(
        load_data: list[dict],
        geographical_unit_code: GeographicalUnitCode,
        regulator: RegulatorType,
):
    """
    load_data: dict or list of dict
    """

    session = get_db_session(database_url=settings.DATABASE_URL)
    load_data_repository = LoadDataRepository(session=session)
    try:
        load_data_repository.add_new_load_data(load_data=load_data)
    except RuntimeError as e:
        print(e)
    else:
        session.close()

    last_valid_data_ending = load_data[-1]['end_datetime']  # data points must be ordered
    update_geographical_unit(code=geographical_unit_code,
                             regulator=regulator,
                             last_valid_data_ending=last_valid_data_ending)


def get_geographical_unit(entity_code: GeographicalUnitCode, regulator: RegulatorType) -> GeographicalUnitEntity:
    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    geographical_unit = None

    try:
        geographical_unit = geographical_unit_repository.get_geographical_unit_from_code(code=entity_code,
                                                                                         regulator=regulator)
    except RuntimeError as e:
        print(e)
    else:
        session.close()

    return geographical_unit


def fetch_and_add_new_load_data(
        entity_code: GeographicalUnitCode,
        regulator: RegulatorType,
        start_datetime: datetime.datetime,
        end_datetime: datetime.datetime
):
    geographical_unit = get_geographical_unit(entity_code=entity_code, regulator=regulator)

    match regulator:
        case RegulatorType.ENTSOE:
            data_client = ENTSOEClient(token=settings.ENTSOE_TOKEN)
        case _:
            raise RuntimeError('Only ENTSOE Data Client is implemented!')

    data_list = data_client.get_load_data(entity_code=entity_code.value,
                                          start_datetime=start_datetime,
                                          end_datetime=end_datetime)

    if len(data_list) > 0:
        # Updates data_list in-place
        _ = [
            x.update(
                {
                    'created_by_id': 1,
                    'updated_by_id': 1,
                    'created_at': datetime.datetime.now(datetime.timezone.utc),
                    'updated_at': datetime.datetime.now(datetime.timezone.utc),
                    'geographical_unit_id': geographical_unit.id,
                }
            ) for x in data_list
        ]
        add_new_load_data(load_data=data_list, geographical_unit_code=entity_code, regulator=regulator)


def sync_load_data(entity_code: GeographicalUnitCode, regulator: RegulatorType):
    MAX_QUERY_DAYS = 180
    ABSOLUTE_BEGINNING = datetime.datetime(year=2015, month=1, day=1, hour=0, minute=0, tzinfo=datetime.timezone.utc)

    geographical_unit = get_geographical_unit(entity_code=entity_code, regulator=regulator)

    if geographical_unit.last_valid_data_ending is None:
        geographical_unit.last_valid_data_ending = ABSOLUTE_BEGINNING

    current_datetime = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)

    while current_datetime - geographical_unit.last_valid_data_ending > datetime.timedelta(days=MAX_QUERY_DAYS):
        start_datetime = geographical_unit.last_valid_data_ending
        end_datetime = start_datetime + datetime.timedelta(days=MAX_QUERY_DAYS)

        fetch_and_add_new_load_data(entity_code=entity_code,
                                    regulator=regulator,
                                    start_datetime=start_datetime,
                                    end_datetime=end_datetime)
        geographical_unit = get_geographical_unit(entity_code=entity_code, regulator=regulator)
    else:
        start_datetime = geographical_unit.last_valid_data_ending
        end_datetime = current_datetime
        fetch_and_add_new_load_data(entity_code=entity_code,
                                    regulator=regulator,
                                    start_datetime=start_datetime,
                                    end_datetime=end_datetime)


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

    for geo_unit in geographical_units:
        print(f'Syncing: {geo_unit.name} - {geo_unit.code.value}')
        sync_load_data(entity_code=geo_unit.code, regulator=RegulatorType.ENTSOE)


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
    'update_geographical_unit',
    'sync_load_data',
    'sync_all_data',
]
