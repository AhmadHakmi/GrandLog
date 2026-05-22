from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.maintenance_schema import (
    MaintenanceCreate,
    MaintenanceResponse
)
from app.services import maintenance_service

router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post("/", response_model=MaintenanceResponse)
def create_maintenance(
    maintenance_data: MaintenanceCreate,
    db: Session = Depends(get_db)
):
    return maintenance_service.create_maintenance(
        db,
        maintenance_data
    )


@router.get("/", response_model=list[MaintenanceResponse])
def get_all_maintenance(
    db: Session = Depends(get_db)
):
    return maintenance_service.get_all_maintenance(db)