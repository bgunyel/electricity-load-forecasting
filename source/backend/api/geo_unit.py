import datetime

from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity
from backend.service.db.models.enums import GeographicalUnitCode, RegulatorType
from backend.service.db.repositories.geographical_unit_repository import GeographicalUnitRepository
from backend.service.utils.get_db_session import get_db_session
from config import settings


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
        print(f'Successfully added: {geographical_unit}')
    finally:
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
        print(f'Successfully updated: {code.value} - {regulator.value} with {last_valid_data_ending}')
    finally:
        session.close()


def get_geographical_unit(entity_code: GeographicalUnitCode, regulator: RegulatorType) -> GeographicalUnitEntity:
    session = get_db_session(database_url=settings.DATABASE_URL)
    geographical_unit_repository = GeographicalUnitRepository(session=session)
    geographical_unit = None

    try:
        geographical_unit = geographical_unit_repository.get_geographical_unit_from_code(code=entity_code,
                                                                                         regulator=regulator)
    except RuntimeError as e:
        print(e)
    finally:
        session.close()

    return geographical_unit
