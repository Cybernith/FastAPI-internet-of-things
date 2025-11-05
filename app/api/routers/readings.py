from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.reading import ReadingCreate, ReadingUpdate, ReadingOut
from app.repositories.reading import ReadingRepository

router = APIRouter(prefix="/readings", tags=["Readings"])


@router.post("/", response_model=ReadingOut, status_code=status.HTTP_201_CREATED)
def create_reading(payload: ReadingCreate, db: Session = Depends(get_db)):
    repo = ReadingRepository(db)
    return repo.create(payload)


@router.get("/", response_model=list)
def list_readings(skip: int = 0, limit: int = 100, sensor_id: int = None, db: Session = Depends(get_db)):
    repo = ReadingRepository(db)
    return repo.list(skip, limit, sensor_id)


@router.get("/{reading_id}", response_model=ReadingOut)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    repo = ReadingRepository(db)
    obj = repo.get(reading_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Reading not found")
    return obj


@router.put("/{reading_id}", response_model=ReadingOut)
def update_reading(reading_id: int, payload: ReadingUpdate, db: Session = Depends(get_db)):
    repo = ReadingRepository(db)
    obj = repo.update(reading_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Reading not found")
    return obj


@router.delete("/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(reading_id: int, db: Session = Depends(get_db)):
    repo = ReadingRepository(db)
    repo.delete(reading_id)
    return None
