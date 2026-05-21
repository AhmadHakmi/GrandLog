from sqlalchemy import Column, Integer, String

from app.database.session import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    nickname = Column(String)
    current_mileage = Column(Integer, default=0)
