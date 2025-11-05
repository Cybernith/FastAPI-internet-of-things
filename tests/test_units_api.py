def test_units_crud_path(client):
    # CREATE
    response = client.post("/units/", json={"name": "Celsius", "symbol": "°C"})
    assert response.status_code == 201
    created = response.json()
    unit_id = created["id"]
    assert created["name"] == "Celsius"
    assert created["symbol"] == "°C"

    # RETRIEVE
    response = client.get("/units/%s" % unit_id)
    assert response.status_code == 200
    assert response.json()["name"] == "Celsius"

    # LIST RETRIEVE
    response = client.get("/units/")
    assert response.status_code == 200
    items = response.json()
    assert any(x["id"] == unit_id for x in items)

    # UPDATE
    response = client.put("/units/%s" % unit_id, json={"name": "Cel", "symbol": "°C"})
    assert response.status_code == 200
    assert response.json()["name"] == "Cel"

    # DELETE
    response = client.delete("/units/%s" % unit_id)
    assert response.status_code == 204


def test_units_not_found(client):
    response = client.get("/units/999999")
    assert response.status_code == 404
    assert response.json().get("detail") == "Unit not found"
