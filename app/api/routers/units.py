from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.unit import UnitCreate, UnitUpdate, UnitOut
from app.repositories.unit import UnitRepository
from app.services.unit import UnitService

router = APIRouter(prefix="/units", tags=["Units"])


def get_service(db: Session = Depends(get_db)):
    return UnitService(UnitRepository(db))


@router.post("/", response_model=UnitOut, status_code=status.HTTP_201_CREATED)
def create_unit(payload: UnitCreate, service: UnitService = Depends(get_service)):
    return service.create_unit(payload)


@router.get("/", response_model=list[UnitOut])
def list_units(skip: int = 0, limit: int = 100, service: UnitService = Depends(get_service)):
    return service.list_units(skip, limit)


@router.get("/{unit_id}", response_model=UnitOut)
def get_unit(unit_id: int, service: UnitService = Depends(get_service)):
    try:
        return service.get_unit(unit_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Unit not found")


@router.put("/{unit_id}", response_model=UnitOut)
def update_unit(unit_id: int, payload: UnitUpdate, service: UnitService = Depends(get_service)):
    try:
        return service.update_unit(unit_id, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Unit not found")


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_unit(unit_id: int, service: UnitService = Depends(get_service)):
    service.delete_unit(unit_id)
