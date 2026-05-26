from sqlalchemy.orm import Session

from app.repositories import fuel_repository
from app.schemas.fuel_schema import FuelLogCreate


def create_fuel_log(db: Session, fuel_data: FuelLogCreate):
    fuel_log = fuel_repository.create_fuel_log(
        db,
        fuel_data
    )

    total_cost = (
        fuel_log.liters * fuel_log.fuel_price
    )

    return {
        "id": fuel_log.id,
        "vehicle_id": fuel_log.vehicle_id,
        "liters": fuel_log.liters,
        "fuel_price": fuel_log.fuel_price,
        "odometer": fuel_log.odometer,
        "total_cost": total_cost
    }


def get_all_fuel_logs(db: Session):
    logs = fuel_repository.get_all_fuel_logs(db)

    result = []

    for log in logs:
        result.append({
            "id": log.id,
            "vehicle_id": log.vehicle_id,
            "liters": log.liters,
            "fuel_price": log.fuel_price,
            "odometer": log.odometer,
            "total_cost": log.liters * log.fuel_price
        })

    return result


def calculate_fuel_economy(
    db: Session,
    vehicle_id: int
):
    logs = fuel_repository.get_vehicle_fuel_logs(
        db,
        vehicle_id
    )

    if len(logs) < 2:
        return {
            "message": "Not enough fuel logs"
        }

    first_log = logs[0]
    last_log = logs[-1]

    distance = (
        last_log.odometer - first_log.odometer
    )

    total_liters = sum(
        log.liters for log in logs
    )

    fuel_economy = (
        distance / total_liters
    )

    return {
        "vehicle_id": vehicle_id,
        "distance_km": distance,
        "total_liters": total_liters,
        "km_per_liter": round(fuel_economy, 2)
    }