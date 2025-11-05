from pydantic import BaseModel, Field
from typing import Optional


class SensorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    unit_id: int
    location: Optional[str] = Field(None, max_length=200)


class SensorUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=120)
    unit_id: Optional[int] = None
    location: Optional[str] = Field(None, max_length=200)


class SensorOut(BaseModel):
    id: int
    name: str
    unit_id: int
    location: Optional[str]

