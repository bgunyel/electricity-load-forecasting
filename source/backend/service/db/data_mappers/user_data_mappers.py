from backend.service.db.entities.user_entities import UserEntity
from backend.service.db.models.user import User


def user_model_to_entity(instance: User) -> UserEntity:
    return UserEntity(id=instance.id,
                      name=instance.name,
                      created_at=instance.created_at,
                      updated_at=instance.updated_at,
                      email=instance.email,
                      is_active=instance.is_active,
                      created_by_id=instance.created_by_id,
                      updated_by_id=instance.updated_by_id)


def user_entity_to_model_dict(entity: UserEntity) -> dict:
    return {
        'id': entity.id,
        'name': entity.name,
        'created_at': entity.created_at,
        'updated_at': entity.updated_at,
        'is_active': entity.is_active,
        'created_by_id': entity.created_by_id,
        'updated_by_id': entity.updated_by_id,
        'email': entity.email
    }
