from pydantic import BaseModel, ConfigDict, Field


class MaintenanceBase(BaseModel):
    vehicle_id: int
    service_type: str
    last_service_mileage: int = Field(ge=0)
    service_interval_km: int = Field(gt=0)
    notes: str | None = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceResponse(MaintenanceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    next_service_due: int
