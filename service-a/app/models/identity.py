from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str
    created_at: datetime


@dataclass(frozen=True)
class Vehicle:
    id: int
    user_id: int
    plate: str
    vehicle_type: str
    active: bool
    created_at: datetime
