# app/services/reading_service.py

from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from app.repositories.reading import ReadingRepository
from app.domain.reading import Reading
from app.schemas.reading import ReadingCreate, ReadingUpdate
from app.exceptions import NotFoundError, ForeignKeyError

class ReadingService:
    def __init__(self, repo: ReadingRepository):
        self.repo = repo

    def _entity_to_dict(self, entity: Reading) -> Dict:
        return {
            "id": entity.id,
            "sensor_id": entity.sensor_id,
            "value": entity.value,  # Decimal preserved — Pydantic will format
            "observed_at": entity.observed_at,
        }

    def list(self, skip: int = 0, limit: int = 100, sensor_id: Optional[int] = None) -> List[Dict]:
        entities = self.repo.list(skip, limit, sensor_id)
        return [self._entity_to_dict(e) for e in entities]

    def get(self, id: int) -> Dict:
        e = self.repo.get(id)
        if not e:
            raise NotFoundError("Reading not found")
        return self._entity_to_dict(e)

    def create(self, payload: ReadingCreate) -> Dict:
        # Build domain entity (id 0 — DB will assign)
        observed_at = payload.observed_at or datetime.utcnow()
        e = Reading(id=0, sensor_id=payload.sensor_id, value=payload.value, observed_at=observed_at)
        try:
            created = self.repo.create(e)
            return self._entity_to_dict(created)
        except IntegrityError as exc:
            # تشخیص خطای FK (Postgres psycopg) یا پیام محتوا
            msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
            if "foreign key" in msg.lower() or "fkey" in msg.lower():
                raise ForeignKeyError("sensor_id does not exist")
            raise

    def update(self, id: int, payload: ReadingUpdate) -> Dict:
        existing = self.repo.get(id)
        if not existing:
            raise NotFoundError("Reading not found")

        # اعمال تغییرات دامنه
        if payload.value is not None:
            existing.update_value(payload.value)
        if payload.observed_at is not None:
            existing.set_observed_at(payload.observed_at)

        try:
            updated = self.repo.update(existing)
            if not updated:
                raise NotFoundError("Reading not found")
            return self._entity_to_dict(updated)
        except IntegrityError as exc:
            msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
            if "foreign key" in msg.lower() or "fkey" in msg.lower():
                raise ForeignKeyError("sensor_id does not exist")
            raise

    def delete(self, id: int) -> None:
        existing = self.repo.get(id)
        if not existing:
            raise NotFoundError("Reading not found")
        rowcount = self.repo.delete(id)
        if rowcount == 0:
            raise NotFoundError("Reading not found")
