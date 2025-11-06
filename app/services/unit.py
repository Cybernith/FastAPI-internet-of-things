from app.domain.unit import Unit
from app.repositories.unit import UnitRepository
from app.schemas.unit import UnitCreate, UnitUpdate


class UnitService:
    def __init__(self, repo: UnitRepository):
        self.repo = repo

    def list_units(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def get_unit(self, id: int) -> Unit:
        unit = self.repo.get(id)
        if not unit:
            raise ValueError("Unit not found")
        return unit

    def create_unit(self, payload: UnitCreate) -> Unit:
        unit = Unit(id=0, name=payload.name, symbol=payload.symbol)
        return self.repo.create(unit)

    def update_unit(self, id: int, payload: UnitUpdate) -> Unit:
        unit = self.get_unit(id)
        if payload.name is not None:
            unit.rename(payload.name)
        if payload.symbol is not None:
            unit.change_symbol(payload.symbol)
        return self.repo.update(unit)

    def delete_unit(self, id: int):
        self.repo.delete(id)
