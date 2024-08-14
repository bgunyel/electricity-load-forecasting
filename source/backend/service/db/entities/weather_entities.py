import datetime
from dataclasses import dataclass


@dataclass
class WeatherStationEntity:
    id: int
    code: str
    name: str
    geographical_unit_id: int
    longitude: float
    latitude: float
    elevation: float
    is_active: bool
    archive_begin: datetime.date
    archive_end: datetime.date
    last_valid_data_ending: datetime.datetime
    created_by_id: int
    created_at: datetime.datetime
    updated_by_id: int
    updated_at: datetime.datetime


@dataclass
class WeatherDataEntity:
    id: int
    station_id: int
    measured_at: datetime.datetime
    temperature_celsius: float
    dewpoint_celsius: float
    relative_humidity: float
    wind_direction: float
    wind_speed: float
    pressure_altimeter: float
    feel_celsius: float
    created_by_id: int
    updated_by_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
