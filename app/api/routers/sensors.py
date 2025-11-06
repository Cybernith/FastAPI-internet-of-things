from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.sensor import SensorCreate, SensorUpdate, SensorOut
from app.services.sensor import SensorService

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(payload: SensorCreate, db: Session = Depends(get_db)):
    service = SensorService(db)
    return service.create_sensor(payload)


@router.get("/", response_model=list[SensorOut])
def list_sensors(skip: int = 0, limit: int = 100, unit_id: int | None = None, db: Session = Depends(get_db)):
    service = SensorService(db)
    return service.list_sensors(skip, limit, unit_id)


@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    service = SensorService(db)
    sensor = service.get_sensor(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.put("/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: int, payload: SensorUpdate, db: Session = Depends(get_db)):
    service = SensorService(db)
    sensor = service.update_sensor(sensor_id, payload)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    service = SensorService(db)
    service.delete_sensor(sensor_id)
