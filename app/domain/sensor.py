from typing import Optional


class Sensor:
    def __init__(self, id: int, name: str, unit_id: int, location: Optional[str] = None):
        self.id = id
        self.name = name
        self.unit_id = unit_id
        self.location = location

    def update_name(self, name: str):
        if not name:
            raise ValueError("name cannot be empty")
        self.name = name

    def update_unit(self, unit_id: int):
        self.unit_id = unit_id

    def update_location(self, location: Optional[str]):
        self.location = location
