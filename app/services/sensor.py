from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.repositories.sensor import SensorRepository
from app.schemas.sensor import SensorCreate, SensorUpdate


class SensorService:
    def __init__(self, db: Session):
        self.repo = SensorRepository(db)

    def list_sensors(self, skip: int, limit: int, unit_id: Optional[int]) -> List[Dict]:
        return self.repo.list(skip, limit, unit_id)

    def get_sensor(self, sensor_id: int) -> Optional[Dict]:
        return self.repo.get(sensor_id)

    def create_sensor(self, payload: SensorCreate) -> Dict:
        return self.repo.create(payload)

    def update_sensor(self, sensor_id: int, payload: SensorUpdate) -> Optional[Dict]:
        return self.repo.update(sensor_id, payload)

    def delete_sensor(self, sensor_id: int) -> None:
        return self.repo.delete(sensor_id)
