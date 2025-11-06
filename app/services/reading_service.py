from typing import Optional, List, Dict
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.exc import IntegrityError
from app.repositories.reading import ReadingRepository
from app.domain.reading import Reading
from app.schemas.reading import ReadingCreate, ReadingUpdate
from app.exceptions import NotFoundError, ForeignKeyError


class ReadingService:
    def __init__(self, repository: ReadingRepository):
        self.repository = repository

    def entity_to_dict(self, entity: Reading) -> Dict:
        return {
            "id": entity.id,
            "sensor_id": entity.sensor_id,
            "value": entity.value,
            "observed_at": entity.observed_at,
        }

    def list(self, skip: int = 0, limit: int = 100, sensor_id: Optional[int] = None) -> List[Dict]:
        entities = self.repository.list(skip, limit, sensor_id)
        return [self.entity_to_dict(e) for e in entities]

    def get(self, id: int) -> Dict:
        e = self.repository.get(id)
        if not e:
            raise NotFoundError("Reading not found")
        return self.entity_to_dict(e)

    def create(self, payload: ReadingCreate) -> Dict:
        observed_at = payload.observed_at or datetime.now(timezone.utc)
        e = Reading(sensor_id=payload.sensor_id, value=payload.value, observed_at=observed_at)
        try:
            created = self.repository.create(e)
            return self.entity_to_dict(created)
        except IntegrityError as exc:
            message = str(exc.orig) if hasattr(exc, "orig") else str(exc)
            if "foreign key" in message.lower() or "fkey" in message.lower():
                raise ForeignKeyError("sensor_id does not exist")
            raise

    def update(self, id: int, payload: ReadingUpdate) -> Dict:
        existing = self.repository.get(id)
        if not existing:
            raise NotFoundError("Reading not found")

        if payload.value is not None:
            existing.update_value(payload.value)
        if payload.observed_at is not None:
            existing.set_observed_at(payload.observed_at)

        try:
            updated = self.repository.update(existing)
            if not updated:
                raise NotFoundError("Reading not found")
            return self.entity_to_dict(updated)
        except IntegrityError as exc:
            message = str(exc.orig) if hasattr(exc, "orig") else str(exc)
            if "foreign key" in message.lower() or "fkey" in message.lower():
                raise ForeignKeyError("sensor_id does not exist")
            raise

    def delete(self, id: int) -> None:
        existing = self.repository.get(id)
        if not existing:
            raise NotFoundError("Reading not found")
        rowcount = self.repository.delete(id)
        if rowcount == 0:
            raise NotFoundError("Reading not found")
