from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from backend.service.db.models.base import ObjectBase


class WeatherStation(ObjectBase):
    __tablename__ = "weather_stations"

    code = Column("code", String, nullable=False, unique=True)
    geographical_unit_id = Column("geographical_unit_id", ForeignKey("geographical_units.id", ondelete="SET NULL"))
    longitude = Column("longitude", Float, nullable=False)
    latitude = Column("latitude", Float, nullable=False)
    elevation = Column("elevation", Float, nullable=False)
    is_active = Column("is_active", Boolean, nullable=False, default=True)
    archive_begin = Column("archive_begin", Date, nullable=False)
    archive_end = Column("archive_end", Date, nullable=True)
    last_valid_data_ending = Column("last_valid_data_ending", DateTime(timezone=True), nullable=True)
    created_by_id = Column("created_by_id", ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_id = Column("updated_by_id", ForeignKey("users.id", ondelete="SET NULL"))

    created_by = relationship(
        argument="User", remote_side="User.id", primaryjoin="WeatherStation.created_by_id == User.id"
    )

    updated_by = relationship(
        argument="User", remote_side="User.id", primaryjoin="WeatherStation.updated_by_id == User.id"
    )

    geographical_unit = relationship(
        argument="GeographicalUnit",
        remote_side="GeographicalUnit.id",
        primaryjoin="WeatherStation.geographical_unit_id == GeographicalUnit.id"
    )
