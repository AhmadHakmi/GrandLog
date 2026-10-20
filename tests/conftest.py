import os

# Point the app at an in-memory database before any app module is imported,
# so the test run can never read or write the real grandlog.db.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.database.init_db  # noqa: F401  (registers every model on Base)
from app.database.dependencies import get_db
from app.database.session import Base
from app.main import app


@pytest.fixture
def db_session():
    # StaticPool keeps one connection, so every session sees the same
    # in-memory database. Each test gets a fresh, empty database.
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Not used as a context manager, so the app's startup hook (init_db)
    # does not run; the test database is set up by db_session instead.
    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def create_vehicle(client):
    def _create_vehicle(**overrides):
        payload = {"make": "Toyota", "model": "Corolla", "year": 2020}
        payload.update(overrides)
        response = client.post("/vehicles/", json=payload)
        assert response.status_code == 200, response.text
        return response.json()

    return _create_vehicle
