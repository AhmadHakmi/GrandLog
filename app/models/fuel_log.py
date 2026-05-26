from sqlalchemy import Column, Float, ForeignKey, Integer

from app.database.session import Base


class FuelLog(Base):
    __tablename__ = "fuel_logs"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    liters = Column(Float, nullable=False)

    fuel_price = Column(Float, nullable=False)

    odometer = Column(Integer, nullable=False)
