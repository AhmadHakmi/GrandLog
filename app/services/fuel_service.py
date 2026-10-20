from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import fuel_repository
from app.schemas.fuel_schema import FuelLogCreate
from app.services import vehicle_service


def create_fuel_log(db: Session, fuel_data: FuelLogCreate):
    vehicle_service.get_vehicle_by_id(db, fuel_data.vehicle_id)
    return fuel_repository.create_fuel_log(db, fuel_data)


def get_all_fuel_logs(db: Session):
    return fuel_repository.get_all_fuel_logs(db)


def calculate_fuel_economy(db: Session, vehicle_id: int):
    vehicle_service.get_vehicle_by_id(db, vehicle_id)
    logs = fuel_repository.get_vehicle_fuel_logs(db, vehicle_id)

    if len(logs) < 2:
        raise HTTPException(status_code=422, detail="Not enough fuel logs")

    first_log = logs[0]
    last_log = logs[-1]

    distance = last_log.odometer - first_log.odometer

    # Full-tank method: the first fill was burned before the measured distance.
    total_liters = sum(log.liters for log in logs[1:])

    if distance <= 0 or total_liters <= 0:
        raise HTTPException(
            status_code=422, detail="Fuel logs do not cover any distance"
        )

    fuel_economy = distance / total_liters

    return {
        "vehicle_id": vehicle_id,
        "distance_km": distance,
        "total_liters": total_liters,
        "km_per_liter": round(fuel_economy, 2),
    }
