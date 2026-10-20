from pydantic import BaseModel, ConfigDict, Field


class FuelLogBase(BaseModel):
    vehicle_id: int
    liters: float = Field(gt=0)
    fuel_price: float = Field(gt=0)
    odometer: int = Field(ge=0)


class FuelLogCreate(FuelLogBase):
    pass


class FuelLogResponse(FuelLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    total_cost: float


class FuelEconomyResponse(BaseModel):
    vehicle_id: int
    distance_km: int
    total_liters: float
    km_per_liter: float
