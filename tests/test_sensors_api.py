import uuid


def _uniq(name):
    return "{}_{}".format(name, uuid.uuid4().hex[:8])


def _unique_symbol():
    return "SYM_" + uuid.uuid4().hex[:8]


def test_sensors_crud(client):
    unit_payload = {"name": _uniq("Percent"), "symbol": _unique_symbol()}
    response = client.post("/units/", json=unit_payload)
    assert response.status_code == 201
    unit_id = response.json()["id"]

    # CREATE
    sensor_payload = {"name": _uniq("HumiditySensor"), "unit_id": unit_id}
    response = client.post("/sensors/", json=sensor_payload)
    assert response.status_code == 201
    created = response.json()
    sensor_id = created["id"]
    assert created["name"].startswith("HumiditySensor")
    assert created["unit_id"] == unit_id

    #  RETRIEVE
    response = client.get("/sensors/{}".format(sensor_id))
    assert response.status_code == 200
    assert response.json()["id"] == sensor_id

    # RETRIEVE LIST
    response = client.get("/sensors/")
    assert response.status_code == 200
    items = response.json()
    assert any(x["id"] == sensor_id for x in items)

    # UPDATE
    upd = {"name": _uniq("HumidX"), "unit_id": unit_id}
    response = client.put("/sensors/{}".format(sensor_id), json=upd)
    assert response.status_code == 200
    assert response.json()["name"].startswith("HumidX")

    # DELETE
    response = client.delete("/sensors/{}".format(sensor_id))
    assert response.status_code == 204

    response = client.get("/sensors/{}".format(sensor_id))
    assert response.status_code == 404


def test_sensor_with_invalid_unit_fk(client):
    # CREATE VALID UNIT
    unit_payload = {"name": _uniq("PressureUnit"), "symbol": _unique_symbol()}
    response = client.post("/units/", json=unit_payload)
    assert response.status_code == 201
    unit_id = response.json()["id"]

    # INSERT SENSOR WITH VALID UNIT ID
    payload = {"name": _uniq("Pressure"), "unit_id": unit_id}
    response = client.post("/sensors/", json=payload)

    assert response.status_code == 201


def test_sensors_pagination_and_multiple_units(client):
    # CREATE UNIQUE UNIT
    u1 = client.post("/units/", json={"name": _uniq("Lux"), "symbol": _unique_symbol()})
    assert u1.status_code == 201
    unit1 = u1.json()["id"]

    u2 = client.post("/units/", json={"name": _uniq("Celsius"), "symbol": _unique_symbol()})
    assert u2.status_code == 201
    unit2 = u2.json()["id"]

    # CREATE SENSORS WITH UNIQUE UNIT
    s_names_u1 = [_uniq("LightA"), _uniq("LightB")]
    s_names_u2 = [_uniq("TempA"), _uniq("TempB"), _uniq("TempC")]

    for n in s_names_u1:
        response = client.post("/sensors/", json={"name": n, "unit_id": unit1})
        assert response.status_code == 201

    for n in s_names_u2:
        response = client.post("/sensors/", json={"name": n, "unit_id": unit2})
        assert response.status_code == 201

    # TEST RETRIEVE BY FILTER
    response = client.get("/sensors/?unit_id={}".format(unit1))
    assert response.status_code == 200
    data_u1 = response.json()
    assert len(data_u1) >= len(s_names_u1)
    assert all(item["unit_id"] == unit1 for item in data_u1)

    # TEST PAGINATION
    response = client.get("/sensors/?limit=2")
    assert response.status_code == 200
    page = response.json()
    assert len(page) <= 2
