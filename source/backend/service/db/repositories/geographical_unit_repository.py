from sqlalchemy.orm import Session
from sqlalchemy import insert

from backend.service.db.models.geographical_unit import GeographicalUnit
from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity
from backend.service.db.data_mappers.geographical_unit_data_mappers import geographical_unit_model_to_entity


class GeographicalUnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_new_geographical_unit(self, geographical_unit: dict):

        # TODO: Safety checks shall be implemented
        self.__insert_geographical_unit(geographical_unit=geographical_unit)

    def __insert_geographical_unit(self, geographical_unit: dict):
        self.session.execute(
            insert(GeographicalUnit),
            geographical_unit
        )
        self.session.commit()
