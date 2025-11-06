import uuid


def _unique_symbol():
    return "SYM_" + uuid.uuid4().hex[:8]


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
