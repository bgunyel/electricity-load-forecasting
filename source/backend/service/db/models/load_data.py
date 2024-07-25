from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.service.db.models.base import ObjectTimestamps


class LoadData(ObjectTimestamps):
    __tablename__ = "load_data"

    id = Column("id", Integer, primary_key=True)
    start_datetime = Column("start_datetime", DateTime(timezone=True), nullable=False)
    end_datetime = Column("end_datetime", DateTime(timezone=True), nullable=False)
    value = Column("value", Integer, nullable=True)

    geographical_unit_id = Column("geographical_unit_id", ForeignKey("geographical_units.id", ondelete="SET NULL"))

    created_by_id = Column("created_by_id", ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_id = Column("updated_by_id", ForeignKey("users.id", ondelete="SET NULL"))

    created_by = relationship(
        "User", remote_side="User.id", primaryjoin="LoadData.created_by_id == User.id"
    )

    updated_by = relationship(
        "User", remote_side="User.id", primaryjoin="LoadData.updated_by_id == User.id"
    )

    geographical_unit = relationship(
        "GeographicalUnit",
        remote_side="GeographicalUnit.id",
        primaryjoin="LoadData.geographical_unit_id == GeographicalUnit.id"
    )
