import datetime
from dataclasses import dataclass

from backend.service.db.models.enums import GeographicalUnitCode


@dataclass
class LoadDataEntity:
    """Class representing a load data entity."""

    id: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime
    geographical_unit_code: GeographicalUnitCode
    value: int

    created_by_id: int
    updated_by_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
