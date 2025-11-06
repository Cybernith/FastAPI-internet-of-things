from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.db.schema import sensors
from app.domain.sensor import Sensor
from decimal import Decimal


class SensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def to_entity(self, row) -> Sensor:
        return Sensor(
            id=int(row["id"]),
            name=row["name"],
            unit_id=int(row["unit_id"]),
            location=row["location"],
        )

    def list(self, skip: int = 0, limit: int = 100, unit_id: Optional[int] = None) -> List[Sensor]:
        stmt = select(sensors)
        if unit_id is not None:
            stmt = stmt.where(sensors.c.unit_id == unit_id)
        stmt = stmt.offset(skip).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [self.to_entity(r) for r in rows]

    def get(self, id: int) -> Optional[Sensor]:
        row = self.db.execute(select(sensors).where(sensors.c.id == id)).mappings().first()
        return self.to_entity(row) if row else None

    def create(self, sensor: Sensor) -> Sensor:
        stmt = insert(sensors).values(
            name=sensor.name,
            unit_id=sensor.unit_id,
            location=sensor.location
        ).returning(sensors)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return self.to_entity(row)

    def update(self, sensor: Sensor) -> Optional[Sensor]:
        stmt = update(sensors).where(sensors.c.id == sensor.id).values(
            name=sensor.name,
            unit_id=sensor.unit_id,
            location=sensor.location
        ).returning(sensors)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return self.to_entity(row) if row else None

    def delete(self, id: int) -> int:
        result = self.db.execute(delete(sensors).where(sensors.c.id == id))
        self.db.commit()
        return getattr(result, "rowcount", 0)
