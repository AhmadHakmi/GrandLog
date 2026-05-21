from fastapi import FastAPI

from app.database.init_db import init_db

app = FastAPI(title="GrandLog")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "GrandLog API is running"}