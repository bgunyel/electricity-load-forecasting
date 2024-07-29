from sqlalchemy.orm import Session
from sqlalchemy import insert, update

from backend.service.db.models.load_data import LoadData
from backend.service.db.entities.load_data_entities import LoadDataEntity
from backend.service.db.data_mappers.load_data_data_mappers import load_data_model_to_entity


class LoadDataRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_load_data_by_id(self, idx: int) -> LoadDataEntity:
        query_result = (
            self.session.query(LoadData)
            .where(
                LoadData.id.__eq__(idx)
            )
        )
        load_data_list = [load_data_model_to_entity(instance=x) for x in query_result]
        if len(load_data_list) != 1:
            raise RuntimeError(f'Expected 1 geographical unit but found {len(load_data_list)}')
        return load_data_list[0]

    def update_load_data(self, idx: int, update_dict: dict):
        self.session.execute(
            update(LoadData)
            .where(
                LoadData.id.__eq__(idx)
            )
            .values(update_dict)
        )
        self.session.commit()

    def add_new_load_data(self, load_data: list[dict]):
        # TODO: Safety checks shall be implemented
        # Updates load_data (list) in-place
        _ = [
            x.update(
                {
                    'start_datetime': x['start_datetime'].replace(microsecond=0),
                    'end_datetime': x['end_datetime'].replace(microsecond=0),
                    'created_at': x['created_at'].replace(microsecond=0),
                    'updated_at': x['updated_at'].replace(microsecond=0),
                }
            ) for x in load_data
        ]
        self.__insert_load_data(load_data=load_data)

    def __insert_load_data(self, load_data: [dict, list[dict]]):
        self.session.execute(
            insert(LoadData),
            load_data
        )
        self.session.commit()
