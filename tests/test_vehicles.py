import pytest


def test_root_reports_api_running(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "GrandLog API is running"}


def test_create_vehicle_returns_saved_vehicle(client):
    payload = {
        "make": "Honda",
        "model": "Civic",
        "year": 2019,
        "nickname": "Daily",
        "current_mileage": 45000,
    }

    response = client.post("/vehicles/", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["id"], int)
    assert {k: body[k] for k in payload} == payload


def test_create_vehicle_uses_defaults_for_optional_fields(create_vehicle):
    vehicle = create_vehicle()

    assert vehicle["nickname"] is None
    assert vehicle["current_mileage"] == 0


def test_create_vehicle_missing_required_field_is_rejected(client):
    response = client.post("/vehicles/", json={"make": "Toyota", "year": 2020})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "field, value",
    [
        ("year", -5),
        ("year", 0),
        ("year", 1885),
        ("current_mileage", -1),
    ],
)
def test_create_vehicle_rejects_invalid_year_or_mileage(client, field, value):
    payload = {"make": "Toyota", "model": "Corolla", "year": 2020, field: value}

    response = client.post("/vehicles/", json=payload)

    assert response.status_code == 422
    assert client.get("/vehicles/").json() == []


def test_create_vehicle_accepts_earliest_year(create_vehicle):
    vehicle = create_vehicle(year=1886)

    assert vehicle["year"] == 1886


def test_list_vehicles_starts_empty(client):
    response = client.get("/vehicles/")

    assert response.status_code == 200
    assert response.json() == []


def test_list_vehicles_returns_all_created(client, create_vehicle):
    first = create_vehicle(model="Corolla")
    second = create_vehicle(model="Camry")

    response = client.get("/vehicles/")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_get_vehicle_by_id(client, create_vehicle):
    vehicle = create_vehicle()

    response = client.get(f"/vehicles/{vehicle['id']}")

    assert response.status_code == 200
    assert response.json() == vehicle


def test_get_missing_vehicle_returns_404(client):
    response = client.get("/vehicles/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}


def test_update_vehicle_changes_only_sent_fields(client, create_vehicle):
    vehicle = create_vehicle(nickname="Old", current_mileage=1000)

    response = client.put(f"/vehicles/{vehicle['id']}", json={"current_mileage": 1500})

    assert response.status_code == 200
    assert response.json() == {**vehicle, "current_mileage": 1500}


def test_update_vehicle_is_saved(client, create_vehicle):
    vehicle = create_vehicle()

    client.put(f"/vehicles/{vehicle['id']}", json={"nickname": "Weekend car"})

    response = client.get(f"/vehicles/{vehicle['id']}")
    assert response.json()["nickname"] == "Weekend car"


@pytest.mark.parametrize("field", ["make", "model", "year", "current_mileage"])
def test_update_vehicle_rejects_null_for_required_field(client, create_vehicle, field):
    vehicle = create_vehicle()

    response = client.put(f"/vehicles/{vehicle['id']}", json={field: None})

    assert response.status_code == 422
    assert client.get(f"/vehicles/{vehicle['id']}").json() == vehicle


@pytest.mark.parametrize("field, value", [("year", -5), ("current_mileage", -1)])
def test_update_vehicle_rejects_invalid_year_or_mileage(
    client, create_vehicle, field, value
):
    vehicle = create_vehicle()

    response = client.put(f"/vehicles/{vehicle['id']}", json={field: value})

    assert response.status_code == 422
    assert client.get(f"/vehicles/{vehicle['id']}").json() == vehicle


def test_update_vehicle_can_clear_nickname(client, create_vehicle):
    vehicle = create_vehicle(nickname="Old")

    response = client.put(f"/vehicles/{vehicle['id']}", json={"nickname": None})

    assert response.status_code == 200
    assert response.json() == {**vehicle, "nickname": None}


def test_update_missing_vehicle_returns_404(client):
    response = client.put("/vehicles/999", json={"nickname": "Ghost"})

    assert response.status_code == 404


def test_delete_vehicle(client, create_vehicle):
    vehicle = create_vehicle()

    response = client.delete(f"/vehicles/{vehicle['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "Vehicle deleted successfully"}
    assert client.get(f"/vehicles/{vehicle['id']}").status_code == 404


def test_delete_missing_vehicle_returns_404(client):
    response = client.delete("/vehicles/999")

    assert response.status_code == 404


def test_delete_vehicle_also_deletes_its_records(client, create_vehicle):
    vehicle = create_vehicle()
    other = create_vehicle(model="Camry")
    for owner in (vehicle, other):
        client.post(
            "/fuel/",
            json={
                "vehicle_id": owner["id"],
                "liters": 40,
                "fuel_price": 1.5,
                "odometer": 1000,
            },
        )
        client.post(
            "/maintenance/",
            json={
                "vehicle_id": owner["id"],
                "service_type": "Oil change",
                "last_service_mileage": 1000,
                "service_interval_km": 5000,
            },
        )

    client.delete(f"/vehicles/{vehicle['id']}")

    fuel_owners = [log["vehicle_id"] for log in client.get("/fuel/").json()]
    maintenance_owners = [
        record["vehicle_id"] for record in client.get("/maintenance/").json()
    ]
    assert fuel_owners == [other["id"]]
    assert maintenance_owners == [other["id"]]
