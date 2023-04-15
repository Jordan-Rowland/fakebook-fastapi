import os

from fastapi.testclient import TestClient
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app import create_app
from app.config import get_settings, Settings
from app.models import Base, get_db, init_db
from app.services.users import get_current_user

USER_ID = 108


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


def get_current_user_override():
    return {"username": "testUser", "id": USER_ID}


SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_TEST_URL")
engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        yield test_client  # testing happens here


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)
    init_db(engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    app = create_app()

    app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_current_user] = get_current_user_override
    
    def get_db_override():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_db_override
    with TestClient(app) as test_client:

        yield test_client  # testing happens here
