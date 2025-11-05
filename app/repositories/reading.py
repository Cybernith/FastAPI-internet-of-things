from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from datetime import datetime
from app.db.schema import readings
from app.schemas.reading import ReadingCreate, ReadingUpdate


class ReadingRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100, sensor_id: Optional[int] = None) -> List[Dict]:
        stmt = select(readings)
        if sensor_id is not None:
            stmt = stmt.where(readings.c.sensor_id == sensor_id)
        stmt = stmt.order_by(readings.c.observed_at.desc()).offset(skip).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [dict(r) for r in rows]

    def get(self, id: int) -> Optional[Dict]:
        row = self.db.execute(select(readings).where(readings.c.id == id)).mappings().first()
        return dict(row) if row else None

    def create(self, payload: ReadingCreate) -> Dict:
        data = payload.dict()
        if not data.get("observed_at"):
            data["observed_at"] = datetime.utcnow()
        stmt = insert(readings).values(**data).returning(readings)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row)

    def update(self, id: int, payload: ReadingUpdate) -> Optional[Dict]:
        data = {k: v for k, v in payload.dict(exclude_unset=True).items()}
        if not data:
            return self.get(id)
        stmt = update(readings).where(readings.c.id == id).values(**data).returning(readings)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row) if row else None

    def delete(self, id: int) -> None:
        self.db.execute(delete(readings).where(readings.c.id == id))
        self.db.commit()
