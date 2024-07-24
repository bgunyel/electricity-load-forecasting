import datetime
from dataclasses import dataclass


@dataclass
class UserEntity:
    """Class for keeping track of a single user."""

    id: int
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    email: str
    is_active: bool
    created_by_id: int
    updated_by_id: int
    