from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.db.schema import units
from app.schemas.unit import UnitCreate, UnitUpdate
from app.core.pyd import model_to_dict

class UnitRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        stmt = select(units).offset(skip).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [dict(r) for r in rows]

    def get(self, id: int) -> Optional[Dict]:
        stmt = select(units).where(units.c.id == id)
        row = self.db.execute(stmt).mappings().first()
        return dict(row) if row else None

    def create(self, payload: UnitCreate) -> Dict:
        data = model_to_dict(payload)
        stmt = insert(units).values(**data).returning(units)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row)

    def update(self, id: int, payload: UnitUpdate) -> Optional[Dict]:
        data = model_to_dict(payload, exclude_unset=True)
        data = {k: v for k, v in data.items() if v is not None}
        if not data:
            return self.get(id)
        stmt = update(units).where(units.c.id == id).values(**data).returning(units)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return dict(row) if row else None

    def delete(self, id: int) -> None:
        self.db.execute(delete(units).where(units.c.id == id))
        self.db.commit()
