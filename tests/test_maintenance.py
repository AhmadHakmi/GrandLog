import pytest


def maintenance_payload(vehicle_id, **overrides):
    payload = {
        "vehicle_id": vehicle_id,
        "service_type": "Oil change",
        "last_service_mileage": 10000,
        "service_interval_km": 5000,
    }
    payload.update(overrides)
    return payload


def test_create_maintenance_calculates_next_service_due(client, create_vehicle):
    vehicle = create_vehicle()

    response = client.post(
        "/maintenance/",
        json=maintenance_payload(vehicle["id"], notes="Synthetic 5W-30"),
    )

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["id"], int)
    assert body["service_type"] == "Oil change"
    assert body["notes"] == "Synthetic 5W-30"
    assert body["next_service_due"] == 15000


def test_create_maintenance_notes_are_optional(client, create_vehicle):
    vehicle = create_vehicle()

    response = client.post("/maintenance/", json=maintenance_payload(vehicle["id"]))

    assert response.status_code == 200
    assert response.json()["notes"] is None


def test_create_maintenance_for_missing_vehicle_returns_404(client):
    response = client.post("/maintenance/", json=maintenance_payload(999))

    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}


@pytest.mark.parametrize(
    "field, value",
    [
        ("last_service_mileage", -1),
        ("service_interval_km", 0),
        ("service_interval_km", -5000),
    ],
)
def test_create_maintenance_rejects_invalid_mileage(
    client, create_vehicle, field, value
):
    vehicle = create_vehicle()

    response = client.post(
        "/maintenance/", json=maintenance_payload(vehicle["id"], **{field: value})
    )

    assert response.status_code == 422


def test_create_maintenance_accepts_zero_last_service_mileage(client, create_vehicle):
    vehicle = create_vehicle()

    response = client.post(
        "/maintenance/",
        json=maintenance_payload(vehicle["id"], last_service_mileage=0),
    )

    assert response.status_code == 200
    assert response.json()["next_service_due"] == 5000


def test_list_maintenance(client, create_vehicle):
    vehicle = create_vehicle()
    client.post("/maintenance/", json=maintenance_payload(vehicle["id"]))
    client.post(
        "/maintenance/",
        json=maintenance_payload(vehicle["id"], service_type="Tire rotation"),
    )

    response = client.get("/maintenance/")

    assert response.status_code == 200
    assert [r["service_type"] for r in response.json()] == [
        "Oil change",
        "Tire rotation",
    ]
