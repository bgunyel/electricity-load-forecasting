import datetime
from dataclasses import dataclass

from backend.service.db.models.enums import GeographicalUnitCode, GeographicalUnitType, RegulatorType


@dataclass
class GeographicalUnitEntity:
    """Class representing a geographical unit entity."""

    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    code: GeographicalUnitCode
    type: GeographicalUnitType
    regulator: RegulatorType
    is_active: bool
    last_valid_data_ending: datetime.datetime
    created_by_id: int
    updated_by_id: int

