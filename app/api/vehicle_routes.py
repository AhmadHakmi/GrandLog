from fastapi import APIRouter

from app.database.dependencies import DatabaseSession
from app.schemas.vehicle_schema import VehicleCreate, VehicleResponse, VehicleUpdate
from app.services import vehicle_service

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@router.post("/", response_model=VehicleResponse)
def create_vehicle(vehicle_data: VehicleCreate, db: DatabaseSession):
    return vehicle_service.create_vehicle(db, vehicle_data)


@router.get("/", response_model=list[VehicleResponse])
def get_all_vehicles(db: DatabaseSession):
    return vehicle_service.get_all_vehicles(db)


@router.get("/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(vehicle_id: int, db: DatabaseSession):
    return vehicle_service.get_vehicle_by_id(db, vehicle_id)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: DatabaseSession,
):
    return vehicle_service.update_vehicle(db, vehicle_id, vehicle_data)


@router.delete("/{vehicle_id}")
def delete_vehicle(vehicle_id: int, db: DatabaseSession):
    return vehicle_service.delete_vehicle(db, vehicle_id)
