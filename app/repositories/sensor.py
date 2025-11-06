from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.db.schema import sensors
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.core.pyd import model_to_dict


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
        data = model_to_dict(payload)
        stmt = insert(sensors).values(**data).returning(sensors)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row)

    def update(self, id: int, payload: SensorUpdate) -> Optional[Dict]:
        data = model_to_dict(payload, exclude_unset=True)
        data = {k: v for k, v in data.items() if v is not None}
        if not data:
            return self.get(id)
        stmt = update(sensors).where(sensors.c.id == id).values(**data).returning(sensors)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row) if row else None

    def delete(self, id: int) -> None:
        result = self.db.execute(delete(sensors).where(sensors.c.id == id))
        self.db.commit()
        return result.rowcount
