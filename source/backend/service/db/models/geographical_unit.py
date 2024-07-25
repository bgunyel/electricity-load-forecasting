from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from backend.service.db.models.base import ObjectBase
from backend.service.db.models.enums import GeographicalUnitCode, GeographicalUnitType, RegulatorType


class GeographicalUnit(ObjectBase):
    __tablename__ = "geographical_units"

    code = Column("code", Enum(GeographicalUnitCode, values_callable=lambda x: [e.value for e in x]))
    type = Column("type", Enum(GeographicalUnitType, values_callable=lambda x: [e.value for e in x]))
    regulator = Column("regulator", Enum(RegulatorType, values_callable=lambda x: [e.value for e in x]))
    is_active = Column("is_active", Boolean, nullable=False, default=True)
    last_valid_data_ending = Column("last_valid_data_ending", DateTime(timezone=True), nullable=True)
    created_by_id = Column("created_by_id", ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_id = Column("updated_by_id", ForeignKey("users.id", ondelete="SET NULL"))

    created_by = relationship(
        "User", remote_side="User.id", primaryjoin="GeographicalUnit.created_by_id == User.id"
    )

    updated_by = relationship(
        "User", remote_side="User.id", primaryjoin="GeographicalUnit.updated_by_id == User.id"
    )
