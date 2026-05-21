from pydantic import BaseModel


class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    nickname: str | None = None
    current_mileage: int = 0


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    make: str | None = None
    model: str | None = None
    year: int | None = None
    nickname: str | None = None
    current_mileage: int | None = None


class VehicleResponse(VehicleBase):
    id: int

    class Config:
        from_attributes = True
