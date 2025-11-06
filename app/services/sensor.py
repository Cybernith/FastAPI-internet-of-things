from typing import Optional, List, Dict
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.repositories.sensor import SensorRepository
from app.repositories.unit import UnitRepository
from app.domain.sensor import Sensor
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.exceptions import NotFoundError, ForeignKeyError, DuplicateError


class SensorService:
    def __init__(self, db):
        self.db = db
        self.repository = SensorRepository(db)
        self.unit_repository = UnitRepository(db)

    def to_dict(self, e: Sensor) -> Dict:
        return {"id": e.id, "name": e.name, "unit_id": e.unit_id, "location": e.location}

    def list_sensors(self, skip: int = 0, limit: int = 100, unit_id: Optional[int] = None) -> List[Dict]:
        ents = self.repository.list(skip, limit, unit_id)
        return [self.to_dict(e) for e in ents]

    def get_sensor(self, sensor_id: int) -> Dict:
        e = self.repository.get(sensor_id)
        if not e:
            raise NotFoundError("Sensor not found")
        return self.to_dict(e)

    def create_sensor(self, payload: SensorCreate) -> Dict:
        unit = self.unit_repository.get(payload.unit_id)
        if not unit:
            raise ForeignKeyError("Unit does not exist")

        sensor = Sensor(name=payload.name, unit_id=payload.unit_id, location=payload.location)
        try:
            created = self.repository.create(sensor)
            return self.to_dict(created)
        except IntegrityError as exc:
            message = str(getattr(exc, "orig", exc)).lower()
            if "foreign key" in message or "fkey" in message:
                raise ForeignKeyError("Unit does not exist")
            if "unique" in message:
                raise DuplicateError("Unique constraint failed")
            raise

    def update_sensor(self, sensor_id: int, payload: SensorUpdate) -> Dict:
        existing = self.repository.get(sensor_id)
        if not existing:
            raise NotFoundError("Sensor not found")

        if payload.name is not None:
            existing.update_name(payload.name)
        if payload.unit_id is not None:
            unit = self.unit_repository.get(payload.unit_id)
            if not unit:
                raise ForeignKeyError("Unit does not exist")
            existing.update_unit(payload.unit_id)
        if payload.location is not None:
            existing.update_location(payload.location)

        try:
            updated = self.repository.update(existing)
            if not updated:
                raise NotFoundError("Sensor not found")
            return self.to_dict(updated)
        except IntegrityError as exc:
            message = str(getattr(exc, "orig", exc)).lower()
            if "foreign key" in message or "fkey" in message:
                raise ForeignKeyError("Unit does not exist")
            if "unique" in message:
                raise DuplicateError("Unique constraint failed")
            raise

    def delete_sensor(self, sensor_id: int) -> None:
        existing = self.repository.get(sensor_id)
        if not existing:
            raise NotFoundError("Sensor not found")
        rowcount = self.repository.delete(sensor_id)
        if rowcount == 0:
            raise NotFoundError("Sensor not found")
