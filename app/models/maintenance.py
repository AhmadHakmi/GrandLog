from sqlalchemy import Column, ForeignKey, Integer, String

from app.database.session import Base


class Maintenance(Base):
    __tablename__ = "maintenance"

    id = Column(Integer, primary_key=True, index=True)

    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))

    service_type = Column(String, nullable=False)

    last_service_mileage = Column(Integer, nullable=False)

    service_interval_km = Column(Integer, nullable=False)

    notes = Column(String, nullable=True)
