from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.reading import ReadingCreate, ReadingUpdate, ReadingOut
from app.repositories.reading import ReadingRepository
from app.services.reading_service import ReadingService
from app.exceptions import NotFoundError, ForeignKeyError

router = APIRouter(prefix="/readings", tags=["Readings"])


def get_service(db: Session = Depends(get_db)):
    repository = ReadingRepository(db)
    return ReadingService(repository)


@router.post("/", response_model=ReadingOut, status_code=status.HTTP_201_CREATED)
def create_reading(payload: ReadingCreate, service: ReadingService = Depends(get_service)):
    try:
        return service.create(payload)
    except ForeignKeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/", response_model=list[ReadingOut])
def list_readings(skip: int = 0, limit: int = 100, sensor_id: int | None = None, service: ReadingService = Depends(get_service)):
    return service.list(skip, limit, sensor_id)


@router.get("/{reading_id}", response_model=ReadingOut)
def get_reading(reading_id: int, service: ReadingService = Depends(get_service)):
    try:
        return service.get(reading_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/{reading_id}", response_model=ReadingOut)
def update_reading(reading_id: int, payload: ReadingUpdate, service: ReadingService = Depends(get_service)):
    try:
        return service.update(reading_id, payload)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except ForeignKeyError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, service: ReadingService = Depends(get_service)):
    try:
        service.delete(reading_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return None
