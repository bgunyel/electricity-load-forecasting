import datetime

from backend.service.data_clients.entsoe import ENTSOEClient
from backend.service.db.models.enums import GeographicalUnitCode, RegulatorType
from backend.service.db.repositories.load_data_repository import LoadDataRepository
from backend.service.utils.get_db_session import get_db_session
from config import settings
from .geo_unit import update_geographical_unit, get_geographical_unit


def add_new_load_data(
        load_data: list[dict],
        geographical_unit_code: GeographicalUnitCode,
        regulator: RegulatorType,
):
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
        prev_last_valid_data_ending = geographical_unit.last_valid_data_ending

        fetch_and_add_new_load_data(entity_code=entity_code,
                                    regulator=regulator,
                                    start_datetime=start_datetime,
                                    end_datetime=end_datetime)
        geographical_unit = get_geographical_unit(entity_code=entity_code, regulator=regulator)

        if ((geographical_unit.last_valid_data_ending is None) or
                (geographical_unit.last_valid_data_ending == prev_last_valid_data_ending)):
            geographical_unit.last_valid_data_ending = end_datetime

    else:  # of WHILE
        start_datetime = geographical_unit.last_valid_data_ending
        end_datetime = current_datetime
        fetch_and_add_new_load_data(entity_code=entity_code,
                                    regulator=regulator,
                                    start_datetime=start_datetime,
                                    end_datetime=end_datetime)
