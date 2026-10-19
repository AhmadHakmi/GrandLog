from sqlalchemy.orm import Session

from app.repositories import maintenance_repository
from app.schemas.maintenance_schema import MaintenanceCreate
from app.services import vehicle_service


def create_maintenance(db: Session, maintenance_data: MaintenanceCreate):
    vehicle_service.get_vehicle_by_id(db, maintenance_data.vehicle_id)
    return maintenance_repository.create_maintenance(db, maintenance_data)


def get_all_maintenance(db: Session):
    return maintenance_repository.get_all_maintenance(db)
