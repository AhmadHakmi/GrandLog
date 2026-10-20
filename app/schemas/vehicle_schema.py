from pydantic import BaseModel, ConfigDict, Field, field_validator

# The first production automobile (Benz Patent-Motorwagen) dates from 1886.
EARLIEST_YEAR = 1886


class VehicleBase(BaseModel):
    make: str
    model: str
    year: int = Field(ge=EARLIEST_YEAR)
    nickname: str | None = None
    current_mileage: int = Field(default=0, ge=0)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    make: str | None = None
    model: str | None = None
    year: int | None = Field(default=None, ge=EARLIEST_YEAR)
    nickname: str | None = None
    current_mileage: int | None = Field(default=None, ge=0)

    @field_validator("make", "model", "year", "current_mileage")
    @classmethod
    def reject_explicit_null(cls, value):
        # Omitting a field leaves it unchanged (validators skip defaults), but
        # explicitly sending null would erase a required value, so reject it.
        # nickname is excluded because clearing it is allowed.
        if value is None:
            raise ValueError("cannot be null")
        return value


class VehicleResponse(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
