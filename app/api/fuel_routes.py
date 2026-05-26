from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.fuel_schema import (
    FuelLogCreate,
    FuelLogResponse
)
from app.services import fuel_service

router = APIRouter(
    prefix="/fuel",
    tags=["Fuel"]
)


@router.post("/", response_model=FuelLogResponse)
def create_fuel_log(
    fuel_data: FuelLogCreate,
    db: Session = Depends(get_db)
):
    return fuel_service.create_fuel_log(
        db,
        fuel_data
    )


@router.get("/", response_model=list[FuelLogResponse])
def get_all_fuel_logs(
    db: Session = Depends(get_db)
):
    return fuel_service.get_all_fuel_logs(db)


@router.get("/analytics/{vehicle_id}")
def calculate_fuel_economy(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    return fuel_service.calculate_fuel_economy(
        db,
        vehicle_id
    )