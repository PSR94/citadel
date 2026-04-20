from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_container
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def bootstrap_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        get_container().ingestion.ingest_directory(db, trigger="pytest")
    yield


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)

