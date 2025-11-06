from datetime import datetime
from decimal import Decimal
from typing import Optional


class Reading:
    def __init__(self, sensor_id: int, value: Decimal, observed_at: datetime, id: Optional[int] = None):
        self.id = id
        self.sensor_id = sensor_id
        self.value = value
        self.observed_at = observed_at

    def update_value(self, new_value: Decimal):
        self.value = new_value

    def set_observed_at(self, when: datetime):
        self.observed_at = when
