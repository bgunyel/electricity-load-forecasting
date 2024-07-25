from backend.service.db.models.load_data import LoadData
from backend.service.db.entities.load_data_entities import LoadDataEntity


def load_data_model_to_entity(instance: LoadData) -> LoadDataEntity:
    return LoadDataEntity(
        id=instance.id,
        start_datetime=instance.start_datetime,
        end_datetime=instance.end_datetime,
        geographical_unit_code=instance.geographical_unit.code,
        value=instance.value,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
        created_by_id=instance.created_by_id,
        updated_by_id=instance.updated_by_id
    )
