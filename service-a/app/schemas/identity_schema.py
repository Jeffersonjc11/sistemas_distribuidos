from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr


class VehicleCreateRequest(BaseModel):
    user_id: int = Field(gt=0)
    plate: str = Field(min_length=5, max_length=16)
    vehicle_type: str = Field(min_length=2, max_length=30)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime


class VehicleResponse(BaseModel):
    id: int
    user_id: int
    plate: str
    vehicle_type: str
    active: bool
    created_at: datetime


class HealthResponse(BaseModel):
    service: str
    status: str
    database: str
