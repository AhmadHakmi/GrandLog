from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.maintenance_schema import (MaintenanceCreate,
                                            MaintenanceResponse)
from app.services import maintenance_service

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

DatabaseSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=MaintenanceResponse)
def create_maintenance(
    maintenance_data: MaintenanceCreate,
    db: DatabaseSession,
):
    return maintenance_service.create_maintenance(db, maintenance_data)


@router.get("/", response_model=list[MaintenanceResponse])
def get_all_maintenance(db: DatabaseSession):
    return maintenance_service.get_all_maintenance(db)
