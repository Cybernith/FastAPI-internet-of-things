from sqlalchemy.orm import Session
from app.domain.unit import Unit
from app.domain.sensor import Sensor
from app.domain.reading import Reading
from app.repositories.unit import UnitRepository
from app.repositories.sensor import SensorRepository
from app.repositories.reading import ReadingRepository
from datetime import datetime


def run_seed(session: Session):
    unit_repo = UnitRepository(session)
    sensor_repo = SensorRepository(session)
    reading_repo = ReadingRepository(session)

    first_unit = unit_repo.create(Unit(name="Celsius", symbol="°C"))
    second_unit = unit_repo.create(Unit(name="Humidity", symbol="%"))

    first_sensor = sensor_repo.create(Sensor(name="Temp Sensor 1", unit_id=first_unit.id, location="Room 1"))
    second_sensor = sensor_repo.create(Sensor(name="Hum Sensor 1", unit_id=second_unit.id, location="Room 2"))

    reading_repo.create(Reading(sensor_id=first_sensor.id, value=22.5, observed_at=datetime.utcnow()))
    reading_repo.create(Reading(sensor_id=second_sensor.id, value=60.0, observed_at=datetime.utcnow()))

    print("✅ Database seeded!")
