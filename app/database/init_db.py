from app.database.session import Base, engine
from app.models.fuel_log import FuelLog
from app.models.maintenance import Maintenance
from app.models.vehicle import Vehicle


def init_db():
    Base.metadata.create_all(bind=engine)
