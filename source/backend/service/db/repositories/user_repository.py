from sqlalchemy.orm import Session
from sqlalchemy import insert

from backend.service.db.data_mappers.user_data_mappers import user_model_to_entity
from backend.service.db.entities.user_entities import UserEntity
from backend.service.db.models.user import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_users(self) -> list[UserEntity]:
        query_result = (
            self.session.query(User)
            .order_by(User.id)
        )

        users = [user_model_to_entity(instance=x) for x in query_result]
        return users

    def insert_user(self, user: dict):

        """
        reference: https://docs.sqlalchemy.org/en/20/orm/queryguide/dml.html#orm-queryguide-bulk-insert

        {
            'name': 'Name Name',
            'created_at': datetime.datetime.now(datetime.timezone.utc),
            'updated_at': datetime.datetime.now(datetime.timezone.utc),
            'is_active': True,
            'created_by_id': 1,
            'updated_by_id': 1,
            'email': 'name@email.com'
        }
        """

        self.session.execute(
            insert(User),
            user
        )
        self.session.commit()
