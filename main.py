from fastapi import FastAPI

from app.api.vehicle_routes import router as vehicle_router
from app.database.init_db import init_db

app = FastAPI(title="GrandLog")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "GrandLog API is running"}


app.include_router(vehicle_router)
