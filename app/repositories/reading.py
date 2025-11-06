# app/repositories/reading.py

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from datetime import datetime
from decimal import Decimal
from app.db.schema import readings
from app.domain.reading import Reading


class ReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def to_entity(self, row) -> Reading:
        return Reading(
            id=int(row["id"]),
            sensor_id=int(row["sensor_id"]),
            value=Decimal(row["value"]),
            observed_at=row["observed_at"],
        )

    def list(self, skip: int = 0, limit: int = 100, sensor_id: Optional[int] = None) -> List[Reading]:
        stmt = select(readings)
        if sensor_id is not None:
            stmt = stmt.where(readings.c.sensor_id == sensor_id)
        stmt = stmt.order_by(readings.c.observed_at.desc()).offset(skip).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [self.to_entity(r) for r in rows]

    def get(self, id: int) -> Optional[Reading]:
        row = self.db.execute(select(readings).where(readings.c.id == id)).mappings().first()
        return self.to_entity(row) if row else None

    def create(self, reading: Reading) -> Reading:
        data = {
            "sensor_id": reading.sensor_id,
            "value": reading.value,
            "observed_at": reading.observed_at or datetime.utcnow()
        }
        stmt = insert(readings).values(**data).returning(readings)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return self.to_entity(row)

    def update(self, reading: Reading) -> Optional[Reading]:
        data = {
            "sensor_id": reading.sensor_id,
            "value": reading.value,
            "observed_at": reading.observed_at
        }
        stmt = update(readings).where(readings.c.id == reading.id).values(**data).returning(readings)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return self.to_entity(row) if row else None

    def delete(self, id: int) -> int:
        result = self.db.execute(delete(readings).where(readings.c.id == id))
        self.db.commit()
        return getattr(result, "rowcount", 0)
