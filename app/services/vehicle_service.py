from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import vehicle_repository
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate


def create_vehicle(db: Session, vehicle_data: VehicleCreate):
    return vehicle_repository.create_vehicle(db, vehicle_data)


def get_all_vehicles(db: Session):
    return vehicle_repository.get_all_vehicles(db)


def get_vehicle_by_id(db: Session, vehicle_id: int):
    vehicle = vehicle_repository.get_vehicle_by_id(db, vehicle_id)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return vehicle


def update_vehicle(db: Session, vehicle_id: int, vehicle_data: VehicleUpdate):
    vehicle = get_vehicle_by_id(db, vehicle_id)
    return vehicle_repository.update_vehicle(db, vehicle, vehicle_data)


def delete_vehicle(db: Session, vehicle_id: int):
    vehicle = get_vehicle_by_id(db, vehicle_id)
    vehicle_repository.delete_vehicle(db, vehicle)

    return {"message": "Vehicle deleted successfully"}
