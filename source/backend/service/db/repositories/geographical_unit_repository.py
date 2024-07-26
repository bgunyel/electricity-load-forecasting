import datetime

from sqlalchemy.orm import Session
from sqlalchemy import insert, update, and_, or_

from backend.service.db.models.geographical_unit import GeographicalUnit
from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity
from backend.service.db.data_mappers.geographical_unit_data_mappers import geographical_unit_model_to_entity
from backend.service.db.models.enums import GeographicalUnitCode, RegulatorType


class GeographicalUnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_new_geographical_unit(self, geographical_unit: dict):
        # TODO: Safety checks shall be implemented
        self.__insert_geographical_unit(geographical_unit=geographical_unit)

    def update_geographical_unit(self,
                                 code: GeographicalUnitCode,
                                 regulator: RegulatorType,
                                 last_valid_data_ending: datetime.datetime):
        update_dict = {
            'last_valid_data_ending': last_valid_data_ending,
            'updated_at': datetime.datetime.now(datetime.timezone.utc),
            'updated_by_id': 1
        }

        self.session.execute(
            update(GeographicalUnit)
            .where(
                and_(
                    GeographicalUnit.code.__eq__(code.value),
                    GeographicalUnit.regulator.__eq__(regulator.value)
                )
            )
            .values(update_dict)
        )
        self.session.commit()

    def get_id_from_code(self, code: GeographicalUnitCode, regulator: RegulatorType) -> int:
        query_result = (
            self.session.query(GeographicalUnit)
            .where(
                and_(
                    GeographicalUnit.code.__eq__(code.value),
                    GeographicalUnit.regulator.__eq__(regulator.value),
                )
            )
            .order_by(GeographicalUnit.id)
        )
        geographical_units = [geographical_unit_model_to_entity(instance=x) for x in query_result]
        if len(geographical_units) != 1:
            raise RuntimeError(f'Expected 1 geographical unit but found {len(geographical_units)}')
        return geographical_units[0].id

    def __insert_geographical_unit(self, geographical_unit: dict):
        self.session.execute(
            insert(GeographicalUnit),
            geographical_unit
        )
        self.session.commit()
