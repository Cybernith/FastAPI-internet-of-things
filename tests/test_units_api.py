import uuid


def _unique_symbol():
    return "SYM_" + uuid.uuid4().hex[:8]


def _uniq(name):
    return "{}_{}".format(name, uuid.uuid4().hex[:8])



def test_units_crud_path(client):
    unique_name = f"Celsius-{uuid.uuid4().hex[:6]}"
    symbol = _unique_symbol()

    response = client.post("/units/", json={"name": unique_name, "symbol": symbol})
    assert response.status_code == 201
    created = response.json()
    unit_id = created["id"]

    assert created["name"] == unique_name
    assert created["symbol"] == symbol

    # RETRIEVE
    response = client.get(f"/units/{unit_id}")
    assert response.status_code == 200
    assert response.json()["name"] == unique_name

    # LIST
    response = client.get("/units/")
    assert response.status_code == 200
    items = response.json()
    assert any(x["id"] == unit_id for x in items)

    # UPDATE
    response = client.put(f"/units/{unit_id}", json={"name": unique_name + "-x", "symbol": _unique_symbol()})
    assert response.status_code == 200
    assert response.json()["name"] == unique_name + "-x"

    # DELETE
    response = client.delete(f"/units/{unit_id}")
    assert response.status_code == 204


def test_unit_overview(client, _prepare_test_db):
    symbol = _unique_symbol()
    name = _uniq("Unit")
    unit_res = client.post("/units/", json={"name": name, "symbol": symbol})
    unit_id = unit_res.json()["id"]

    sensor_res = client.post("/sensors/", json={"name": "S1", "unit_id": unit_id, "location": "Room"})
    sensor_id = sensor_res.json()["id"]

    client.post("/readings/", json={"sensor_id": sensor_id, "value": 42})

    overview_res = client.get(f"/units/{unit_id}/overview")
    data = overview_res.json()

    assert overview_res.status_code == 200
    assert data["unit_id"] == unit_id
    assert data["sensor_count"] == 1
    assert data["reading_count"] == 1
    assert data["latest_readings"][0]["sensor_id"] == sensor_id
    assert data["latest_readings"][0]["value"] == 42
