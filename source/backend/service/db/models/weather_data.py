from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.service.db.models.base import ObjectTimestamps


class WeatherData(ObjectTimestamps):
    __tablename__ = "weather_data"

    id = Column("id", Integer, primary_key=True)
    station_id = Column("station_id", ForeignKey("weather_stations.id", ondelete="SET NULL"))
    measured_at = Column("measured_at", DateTime(timezone=True), nullable=False)

    temperature_celsius = Column("temperature_celsius", Float, nullable=True)
    dewpoint_celsius = Column("dewpoint_celsius", Float, nullable=True)
    relative_humidity = Column("relative_humidity", Float, nullable=True)
    wind_direction = Column("wind_direction", Float, nullable=True)
    wind_speed = Column("wind_speed", Float, nullable=True)
    pressure_altimeter = Column("pressure_altimeter", Float, nullable=True)
    feel_celsius = Column("feel_celsius", Float, nullable=True)

    created_by_id = Column("created_by_id", ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_id = Column("updated_by_id", ForeignKey("users.id", ondelete="SET NULL"))

    created_by = relationship(
        "User", remote_side="User.id", primaryjoin="WeatherData.created_by_id == User.id"
    )

    updated_by = relationship(
        "User", remote_side="User.id", primaryjoin="WeatherData.updated_by_id == User.id"
    )

    station = relationship(
        "WeatherStation",
        remote_side="WeatherStation.id",
        primaryjoin="WeatherData.station_id == WeatherStation.id"
    )
