from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from backend.service.db.models.base import ObjectBase


class User(ObjectBase):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    is_active = Column("is_active", Boolean, nullable=False, default=True)

    created_by_id = Column("created_by_id", ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_id = Column("updated_by_id", ForeignKey("users.id", ondelete="SET NULL"))

    created_by = relationship(
        "User", remote_side="User.id", primaryjoin="User.created_by_id == User.id"
    )

    updated_by = relationship(
        "User", remote_side="User.id", primaryjoin="User.updated_by_id == User.id"
    )
