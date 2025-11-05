import os
import pathlib
import shutil
import pytest
from fastapi.testclient import TestClient

import app.main as app_main
from app.db.session import engine
from app.db.init_database import init_database

import os
os.environ.setdefault("ENV", "test")
if os.environ.get("ENV") == "test" and "postgresql" in os.environ.get("DATABASE_URL",""):
    raise RuntimeError("Tests must not run against PostgreSQL. Use in-memory SQLite instead.")

TEST_DB_PATH = pathlib.Path("./tests/test.db").resolve()
os.environ["ENV"] = "test"
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_PATH}"


@pytest.fixture(scope="session", autouse=True)
def _prepare_test_db():
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()
    init_database(engine)
    yield
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture(scope="session")
def client():
    with TestClient(app_main.app) as c:
        yield c
