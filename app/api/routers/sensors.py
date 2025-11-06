from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.sensor import SensorCreate, SensorUpdate, SensorOut
from app.services.sensor import SensorService
from app.exceptions import NotFoundError, ForeignKeyError, DuplicateError

router = APIRouter(prefix="/sensors", tags=["Sensors"])


def get_service(db: Session = Depends(get_db)):
    return SensorService(db)


@router.post("/", response_model=SensorOut, status_code=status.HTTP_201_CREATED)
def create_sensor(payload: SensorCreate, service: SensorService = Depends(get_service)):
    try:
        return service.create_sensor(payload)
    except ForeignKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/", response_model=list[SensorOut])
def list_sensors(skip: int = 0, limit: int = 100, unit_id: int | None = None,
                 service: SensorService = Depends(get_service)):
    return service.list_sensors(skip, limit, unit_id)


@router.get("/{sensor_id}", response_model=SensorOut)
def get_sensor(sensor_id: int, service: SensorService = Depends(get_service)):
    try:
        return service.get_sensor(sensor_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{sensor_id}", response_model=SensorOut)
def update_sensor(sensor_id: int, payload: SensorUpdate, service: SensorService = Depends(get_service)):
    try:
        return service.update_sensor(sensor_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ForeignKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{sensor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sensor(sensor_id: int, service: SensorService = Depends(get_service)):
    try:
        service.delete_sensor(sensor_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
