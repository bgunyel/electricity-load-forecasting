import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, update

from backend.service.db.models.geographical_unit import GeographicalUnit
from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity
from backend.service.db.data_mappers.geographical_unit_data_mappers import geographical_unit_model_to_entity
from backend.service.db.models.enums import GeographicalUnitCode


class GeographicalUnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_new_geographical_unit(self, geographical_unit: dict):
        # TODO: Safety checks shall be implemented
        self.__insert_geographical_unit(geographical_unit=geographical_unit)

    def update_geographical_unit(self, code: GeographicalUnitCode, last_valid_data_ending: datetime.datetime):
        update_dict = {
            'last_valid_data_ending': last_valid_data_ending,
            'updated_at': datetime.datetime.now(datetime.timezone.utc),
            'updated_by_id': 1
        }

        self.session.execute(
            update(GeographicalUnit)
            .where(GeographicalUnit.code.__eq__(code.value))
            .values(update_dict)
        )
        self.session.commit()

    def __insert_geographical_unit(self, geographical_unit: dict):
        self.session.execute(
            insert(GeographicalUnit),
            geographical_unit
        )
        self.session.commit()
