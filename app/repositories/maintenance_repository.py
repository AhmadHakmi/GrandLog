from sqlalchemy.orm import Session

from app.models.maintenance import Maintenance
from app.schemas.maintenance_schema import MaintenanceCreate


def create_maintenance(db: Session, maintenance_data: MaintenanceCreate):
    maintenance = Maintenance(**maintenance_data.model_dump())

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return maintenance


def get_all_maintenance(db: Session):
    return db.query(Maintenance).all()
