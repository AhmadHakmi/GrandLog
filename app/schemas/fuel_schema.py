from pydantic import BaseModel


class FuelLogBase(BaseModel):
    vehicle_id: int
    liters: float
    fuel_price: float
    odometer: int


class FuelLogCreate(FuelLogBase):
    pass


class FuelLogResponse(FuelLogBase):
    id: int
    total_cost: float

    class Config:
        from_attributes = True