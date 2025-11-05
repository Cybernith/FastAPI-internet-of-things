from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.unit import UnitCreate, UnitUpdate, UnitOut
from app.repositories.unit import UnitRepository

router = APIRouter(prefix="/units", tags=["Units"])


@router.post("/", response_model=UnitOut, status_code=status.HTTP_201_CREATED)
def create_unit(payload: UnitCreate, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    return repo.create(payload)


@router.get("/", response_model=list)
def list_units(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    return repo.list(skip, limit)


@router.get("/{unit_id}", response_model=UnitOut)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    obj = repo.get(unit_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Unit not found")
    return obj


@router.put("/{unit_id}", response_model=UnitOut)
def update_unit(unit_id: int, payload: UnitUpdate, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    obj = repo.update(unit_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Unit not found")
    return obj


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    repo = UnitRepository(db)
    repo.delete(unit_id)
    return None
