from fastapi import APIRouter

from app.database.dependencies import DatabaseSession
from app.schemas.fuel_schema import (
    FuelEconomyResponse,
    FuelLogCreate,
    FuelLogResponse,
)
from app.services import fuel_service

router = APIRouter(prefix="/fuel", tags=["Fuel"])


@router.post("/", response_model=FuelLogResponse)
def create_fuel_log(fuel_data: FuelLogCreate, db: DatabaseSession):
    return fuel_service.create_fuel_log(db, fuel_data)


@router.get("/", response_model=list[FuelLogResponse])
def get_all_fuel_logs(db: DatabaseSession):
    return fuel_service.get_all_fuel_logs(db)


@router.get("/analytics/{vehicle_id}", response_model=FuelEconomyResponse)
def calculate_fuel_economy(vehicle_id: int, db: DatabaseSession):
    return fuel_service.calculate_fuel_economy(db, vehicle_id)
