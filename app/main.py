from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.fuel_routes import router as fuel_router
from app.api.maintenance_routes import router as maintenance_router
from app.api.vehicle_routes import router as vehicle_router
from app.core.config import settings
from app.database.init_db import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "GrandLog API is running"}


app.include_router(vehicle_router)
app.include_router(maintenance_router)
app.include_router(fuel_router)
