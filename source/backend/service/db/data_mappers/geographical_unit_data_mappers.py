from backend.service.db.models.geographical_unit import GeographicalUnit
from backend.service.db.entities.geographical_unit_entities import GeographicalUnitEntity


def geographical_unit_model_to_entity(instance: GeographicalUnit) -> GeographicalUnitEntity:
    return GeographicalUnitEntity(
        id=instance.id,
        code=instance.code,
        name=instance.name,
        type=instance.type,
        regulator=instance.regulator,
        is_active=instance.is_active,
        last_valid_data_ending=instance.last_valid_data_ending,
        created_at=instance.created_at,
        updated_at=instance.updated_at,
        created_by_id=instance.created_by_id,
        updated_by_id=instance.updated_by_id
    )
