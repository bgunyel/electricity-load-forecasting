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
