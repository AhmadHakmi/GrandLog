from pydantic import BaseModel


class MaintenanceBase(BaseModel):
    vehicle_id: int
    service_type: str
    last_service_mileage: int
    service_interval_km: int
    notes: str | None = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceResponse(MaintenanceBase):
    id: int
    next_service_due: int

    class Config:
        from_attributes = True
