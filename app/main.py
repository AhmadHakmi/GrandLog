from fastapi import FastAPI

from app.api.vehicle_routes import router as vehicle_router
from app.database.init_db import init_db
from app.api.fuel_routes import router as fuel_router

from app.api.maintenance_routes import (
    router as maintenance_router
)

app = FastAPI(title="GrandLog")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "GrandLog API is running"}


app.include_router(vehicle_router)
app.include_router(maintenance_router)
app.include_router(fuel_router)
