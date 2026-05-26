from sqlalchemy.orm import Session

from app.models.fuel_log import FuelLog
from app.schemas.fuel_schema import FuelLogCreate


def create_fuel_log(db: Session, fuel_data: FuelLogCreate):
    fuel_log = FuelLog(**fuel_data.model_dump())

    db.add(fuel_log)
    db.commit()
    db.refresh(fuel_log)

    return fuel_log


def get_all_fuel_logs(db: Session):
    return db.query(FuelLog).all()


def get_vehicle_fuel_logs(db: Session, vehicle_id: int):
    return (
        db.query(FuelLog)
        .filter(FuelLog.vehicle_id == vehicle_id)
        .order_by(FuelLog.odometer)
        .all()
    )