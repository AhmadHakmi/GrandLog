from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import SessionLocal


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


DatabaseSession = Annotated[Session, Depends(get_db)]
