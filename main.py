from fastapi import FastAPI

app = FastAPI(title="GrandLog")


@app.get("/")
def root():
    return {"message": "GrandLog API is running"}