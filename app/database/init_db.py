from app.database.session import Base, engine
from app.models.vehicle import Vehicle
from app.models.maintenance import Maintenance


def init_db():
    Base.metadata.create_all(bind=engine)
