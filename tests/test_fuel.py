import pytest


@pytest.fixture
def add_fuel_log(client):
    def _add_fuel_log(vehicle_id, odometer, liters=40, fuel_price=1.5):
        response = client.post(
            "/fuel/",
            json={
                "vehicle_id": vehicle_id,
                "liters": liters,
                "fuel_price": fuel_price,
                "odometer": odometer,
            },
        )
        assert response.status_code == 200, response.text
        return response.json()

    return _add_fuel_log


def test_create_fuel_log_calculates_total_cost(create_vehicle, add_fuel_log):
    vehicle = create_vehicle()

    log = add_fuel_log(vehicle["id"], odometer=12000, liters=40, fuel_price=1.25)

    assert isinstance(log["id"], int)
    assert log["odometer"] == 12000
    assert log["total_cost"] == pytest.approx(50.0)


def test_create_fuel_log_for_missing_vehicle_returns_404(client):
    response = client.post(
        "/fuel/",
        json={"vehicle_id": 999, "liters": 40, "fuel_price": 1.5, "odometer": 0},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Vehicle not found"}


@pytest.mark.parametrize(
    "field, value",
    [
        ("liters", 0),
        ("liters", -10),
        ("fuel_price", 0),
        ("fuel_price", -1.5),
        ("odometer", -1),
    ],
)
def test_create_fuel_log_rejects_invalid_values(client, create_vehicle, field, value):
    vehicle = create_vehicle()
    payload = {
        "vehicle_id": vehicle["id"],
        "liters": 40,
        "fuel_price": 1.5,
        "odometer": 1000,
    }
    payload[field] = value

    response = client.post("/fuel/", json=payload)

    assert response.status_code == 422


def test_list_fuel_logs(client, create_vehicle, add_fuel_log):
    vehicle = create_vehicle()
    first = add_fuel_log(vehicle["id"], odometer=1000)
    second = add_fuel_log(vehicle["id"], odometer=1500)

    response = client.get("/fuel/")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_fuel_economy_uses_full_tank_method(client, create_vehicle, add_fuel_log):
    vehicle = create_vehicle()
    add_fuel_log(vehicle["id"], odometer=10000, liters=50)  # first fill: ignored
    add_fuel_log(vehicle["id"], odometer=10500, liters=35)
    add_fuel_log(vehicle["id"], odometer=11000, liters=30)

    response = client.get(f"/fuel/analytics/{vehicle['id']}")

    assert response.status_code == 200
    assert response.json() == {
        "vehicle_id": vehicle["id"],
        "distance_km": 1000,
        "total_liters": 65.0,
        "km_per_liter": 15.38,  # 1000 / 65, rounded to 2 places
    }


def test_fuel_economy_sorts_logs_by_odometer(client, create_vehicle, add_fuel_log):
    vehicle = create_vehicle()
    add_fuel_log(vehicle["id"], odometer=11000, liters=30)
    add_fuel_log(vehicle["id"], odometer=10000, liters=50)
    add_fuel_log(vehicle["id"], odometer=10500, liters=35)

    response = client.get(f"/fuel/analytics/{vehicle['id']}")

    assert response.status_code == 200
    assert response.json()["distance_km"] == 1000
    assert response.json()["total_liters"] == 65.0


def test_fuel_economy_ignores_other_vehicles_logs(client, create_vehicle, add_fuel_log):
    vehicle = create_vehicle()
    other = create_vehicle(model="Camry")
    add_fuel_log(vehicle["id"], odometer=1000, liters=40)
    add_fuel_log(vehicle["id"], odometer=1600, liters=40)
    add_fuel_log(other["id"], odometer=50000, liters=60)

    response = client.get(f"/fuel/analytics/{vehicle['id']}")

    assert response.status_code == 200
    assert response.json()["distance_km"] == 600
    assert response.json()["km_per_liter"] == 15.0


@pytest.mark.parametrize("log_count", [0, 1])
def test_fuel_economy_needs_two_logs(client, create_vehicle, add_fuel_log, log_count):
    vehicle = create_vehicle()
    for i in range(log_count):
        add_fuel_log(vehicle["id"], odometer=1000 + i)

    response = client.get(f"/fuel/analytics/{vehicle['id']}")

    assert response.status_code == 422
    assert response.json() == {"detail": "Not enough fuel logs"}


def test_fuel_economy_rejects_logs_with_no_distance(
    client, create_vehicle, add_fuel_log
):
    vehicle = create_vehicle()
    add_fuel_log(vehicle["id"], odometer=5000)
    add_fuel_log(vehicle["id"], odometer=5000)

    response = client.get(f"/fuel/analytics/{vehicle['id']}")

    assert response.status_code == 422
    assert response.json() == {"detail": "Fuel logs do not cover any distance"}


def test_fuel_economy_for_missing_vehicle_returns_404(client):
    response = client.get("/fuel/analytics/999")

    assert response.status_code == 404
