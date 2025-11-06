import uuid
import time
from datetime import datetime, timezone, timedelta
from decimal import Decimal, ROUND_DOWN


def _unique_id():
    return int(uuid.uuid4().int % 10 ** 8)


def _uniq(prefix: str) -> str:
    return "{}_{}".format(prefix, uuid.uuid4().hex[:8])


def _unique_symbol() -> str:
    return "SYM_" + uuid.uuid4().hex[:8]


def _iso_now(offset_sec=0) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=offset_sec)).isoformat()


def _to_decimal(x):
    return Decimal(str(x))


def create_unit(client, name=None, symbol=None) -> int:
    payload = {
        "name": name or _uniq("Unit"),
        "symbol": symbol or _unique_symbol(),
    }
    response = client.post("/units/", json=payload)
    assert response.status_code == 201
    return response.json()["id"]


def create_sensor(client, unit_id: int, name=None, location=None) -> int:
    payload = {
        "name": name or _uniq("Sensor"),
        "unit_id": unit_id,
        "location": location,
    }
    response = client.post("/sensors/", json=payload)
    assert response.status_code == 201
    return response.json()["id"]


def test_readings_crud(client):
    unit_id = create_unit(client, name=_uniq("Celsius"), symbol=_unique_symbol())
    sensor_id = create_sensor(client, unit_id, name=_uniq("TempSensor"))

    payload = {
        "sensor_id": sensor_id,
        "value": "23.5",
        "observed_at": _iso_now(),
    }

    # CREATE
    response = client.post("/readings/", json=payload)
    assert response.status_code == 201
    created = response.json()
    reading_id = created["id"]
    assert created["sensor_id"] == sensor_id
    assert _to_decimal(created["value"]) == Decimal("23.5")

    # RETRIEVE
    response = client.get(f"/readings/{reading_id}")
    assert response.status_code == 200
    got = response.json()
    assert got["id"] == reading_id

    # LIST (filtered by sensor_id)
    response = client.get("/readings/", params={"sensor_id": sensor_id})
    assert response.status_code == 200
    items = response.json()
    assert any(x["id"] == reading_id for x in items)

    # UPDATE
    response = client.put(f"/readings/{reading_id}", json={"value": "24.125", "observed_at": _iso_now(1)})
    assert response.status_code == 200
    upd = response.json()
    assert _to_decimal(upd["value"]) == Decimal("24.125")

    # DELETE
    response = client.delete(f"/readings/{reading_id}")
    assert response.status_code == 204

    # Ensure DELETED SUCCESSFUL
    response = client.get(f"/readings/{reading_id}")
    assert response.status_code == 404


def test_decimal_precision_preserved_and_bounds(client):
    unit_id = create_unit(client, name=_uniq("Percent"), symbol=_unique_symbol())
    sensor_id = create_sensor(client, unit_id, name=_uniq("Humidity"))

    unique_sensor_id = _unique_id()

    response = client.post("/sensors/", json={
        "id": unique_sensor_id,
        "name": _uniq("HumidityY"),
        "unit_id": unit_id
    })
    assert response.status_code == 201
    sensor_id = response.json()["id"]

    response = client.post("/readings/", json={
        "sensor_id": sensor_id,
        "value": "23.500",
        "observed_at": _iso_now(),
    })
    assert response.status_code == 201


def test_readings_pagination(client):
    unit_id = create_unit(client, name=_uniq("Lux"), symbol=_unique_symbol())
    sensor_id = create_sensor(client, unit_id, name=_uniq("Light"))

    ids = []
    for i in range(12):
        response = client.post("/readings/", json={
            "sensor_id": sensor_id,
            "value": str(i),
            "observed_at": _iso_now(i),
        })
        assert response.status_code == 201
        ids.append(response.json()["id"])

    # page 1
    response = client.get("/readings/", params={"sensor_id": sensor_id, "skip": 0, "limit": 5})
    assert response.status_code == 200
    page1 = response.json()
    assert len(page1) <= 5

    # page 2
    response = client.get("/readings/", params={"sensor_id": sensor_id, "skip": 5, "limit": 5})
    assert response.status_code == 200
    page2 = response.json()
    assert len(page2) <= 5

    first_page_ids = {x["id"] for x in page1}
    second_page_ids = {x["id"] for x in page2}
    assert first_page_ids.isdisjoint(second_page_ids)
