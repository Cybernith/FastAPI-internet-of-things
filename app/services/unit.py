from app.domain.unit import Unit
from app.repositories.unit import UnitRepository
from app.repositories.reading import ReadingRepository
from app.repositories.sensor import SensorRepository
from app.schemas.unit import UnitCreate, UnitUpdate
from typing import Dict


class UnitService:
    def __init__(self, repository: UnitRepository):
        self.repository = repository

    def list_units(self, skip: int = 0, limit: int = 100):
        return self.repository.list(skip, limit)

    def get_unit(self, id: int) -> Unit:
        unit = self.repository.get(id)
        if not unit:
            raise ValueError("Unit not found")
        return unit

    def create_unit(self, payload: UnitCreate) -> Unit:
        unit = Unit(name=payload.name, symbol=payload.symbol)
        return self.repository.create(unit)

    def update_unit(self, id: int, payload: UnitUpdate) -> Unit:
        unit = self.get_unit(id)
        if payload.name is not None:
            unit.rename(payload.name)
        if payload.symbol is not None:
            unit.change_symbol(payload.symbol)
        return self.repository.update(unit)

    def delete_unit(self, id: int):
        self.repository.delete(id)

    def overview(self, unit_id: int) -> Dict:
        unit = self.get_unit(unit_id)
        sensors = SensorRepository(self.repository.db).list(unit_id=unit_id)
        sensor_ids = [s.id for s in sensors]

        reading_repo = ReadingRepository(self.repository.db)
        readings = []
        for sid in sensor_ids:
            latest = reading_repo.latest_for_sensor(sid)
            if latest:
                readings.append({
                    "sensor_id": sid,
                    "value": latest.value,
                    "observed_at": latest.observed_at
                })

        return {
            "unit_id": unit.id,
            "name": unit.name,
            "symbol": unit.symbol,
            "sensor_count": len(sensor_ids),
            "reading_count": reading_repo.count_for_unit(unit_id),
            "latest_readings": readings
        }
