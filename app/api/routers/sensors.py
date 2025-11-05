from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.sensor import SensorCreate, SensorUpdate, SensorOut
from app.repositories.sensor import SensorRepository

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(payload: SensorCreate, db: Session = Depends(get_db)):
    repo = SensorRepository(db)
    return repo.create(payload)


@router.get("/", response_model=list)
def list_sensors(skip: int = 0, limit: int = 100, unit_id: int = None, db: Session = Depends(get_db)):
    repo = SensorRepository(db)
    return repo.list(skip, limit, unit_id)


@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: int, db: Session = Depends(get_db)):
    repo = SensorRepository(db)
    obj = repo.get(sensor_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return obj


@router.put("/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: int, payload: SensorUpdate, db: Session = Depends(get_db)):
    repo = SensorRepository(db)
    obj = repo.update(sensor_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return obj


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, db: Session = Depends(get_db)):
    repo = SensorRepository(db)
    repo.delete(sensor_id)
    return None
