from pydantic import BaseModel, Field
from typing import Optional


class UnitCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    symbol: str = Field(..., min_length=1, max_length=16)


class UnitUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    symbol: Optional[str] = Field(None, max_length=16)


class UnitOut(BaseModel):
    id: int
    name: str
    symbol: str
