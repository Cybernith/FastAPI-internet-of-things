from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from decimal import Decimal
from typing import Optional


class ReadingCreate(BaseModel):
    sensor_id: int
    value: Decimal = Field(..., gt=-1e18, lt=1e18)
    observed_at: Optional[datetime] = None


class ReadingUpdate(BaseModel):
    value: Optional[Decimal] = Field(None, gt=-1e18, lt=1e18)
    observed_at: Optional[datetime] = None


class ReadingOut(BaseModel):
    id: int
    sensor_id: int
    value: Decimal
    observed_at: datetime

    @field_serializer("value")
    def _format_value(self, v: Decimal):
        return f"{Decimal(v):.3f}"
