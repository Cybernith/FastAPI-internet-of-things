from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.db.schema import sensors
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100, unit_id: Optional[int] = None) -> List[Dict]:
        stmt = select(sensors)
        if unit_id is not None:
            stmt = stmt.where(sensors.c.unit_id == unit_id)
        stmt = stmt.offset(skip).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [dict(r) for r in rows]

    def get(self, id: int) -> Optional[Dict]:
        row = self.db.execute(select(sensors).where(sensors.c.id == id)).mappings().first()
        return dict(row) if row else None

    def create(self, payload: SensorCreate) -> Dict:
        stmt = insert(sensors).values(**payload.dict()).returning(sensors)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row)

    def update(self, id: int, payload: SensorUpdate) -> Optional[Dict]:
        data = {k: v for k, v in payload.dict(exclude_unset=True).items()}
        if not data:
            return self.get(id)
        stmt = update(sensors).where(sensors.c.id == id).values(**data).returning(sensors)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row) if row else None

    def delete(self, id: int) -> None:
        self.db.execute(delete(sensors).where(sensors.c.id == id))
        self.db.commit()
