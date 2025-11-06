from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from app.db.schema import units
from app.domain.unit import Unit


class UnitRepository:
    def __init__(self, db: Session):
        self.db = db

    def to_entity(self, row) -> Unit:
        return Unit(id=row.id, name=row.name, symbol=row.symbol)

    def list(self, skip: int = 0, limit: int = 100) -> List[Unit]:
        stmt = select(units).offset(skip).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [self.to_entity(r) for r in rows]

    def get(self, id: int) -> Optional[Unit]:
        stmt = select(units).where(units.c.id == id)
        row = self.db.execute(stmt).mappings().first()
        return self.to_entity(row) if row else None

    def create(self, unit: Unit) -> Unit:
        stmt = insert(units).values(name=unit.name, symbol=unit.symbol).returning(units)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return self.to_entity(row)

    def update(self, unit: Unit) -> Optional[Unit]:
        stmt = update(units).where(units.c.id == unit.id).values(
            name=unit.name,
            symbol=unit.symbol
        ).returning(units)
        row = self.db.execute(stmt).mappings().first()
        self.db.commit()
        return self.to_entity(row) if row else None

    def delete(self, id: int):
        self.db.execute(delete(units).where(units.c.id == id))
        self.db.commit()
