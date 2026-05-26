from sqlalchemy.orm import Session

from app.repositories import maintenance_repository
from app.schemas.maintenance_schema import MaintenanceCreate


def create_maintenance(db: Session, maintenance_data: MaintenanceCreate):
    maintenance = maintenance_repository.create_maintenance(db, maintenance_data)

    next_service_due = (
        maintenance.last_service_mileage + maintenance.service_interval_km
    )

    return {**maintenance.__dict__, "next_service_due": next_service_due}


def get_all_maintenance(db: Session):
    maintenance_records = maintenance_repository.get_all_maintenance(db)

    result = []

    for maintenance in maintenance_records:
        next_service_due = (
            maintenance.last_service_mileage + maintenance.service_interval_km
        )

        result.append({**maintenance.__dict__, "next_service_due": next_service_due})

    return result
