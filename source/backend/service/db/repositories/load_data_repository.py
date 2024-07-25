from sqlalchemy.orm import Session
from sqlalchemy import insert

from backend.service.db.models.load_data import LoadData
from backend.service.db.entities.load_data_entities import LoadDataEntity
from backend.service.db.data_mappers.load_data_data_mappers import load_data_model_to_entity


class LoadDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_new_load_data(self, load_data: [dict, list[dict]]):

        # TODO: Safety checks shall be implemented
        self.__insert_load_data(load_data=load_data)

    def __insert_load_data(self, load_data: [dict, list[dict]]):
        self.session.execute(
            insert(LoadData),
            load_data
        )
        self.session.commit()
