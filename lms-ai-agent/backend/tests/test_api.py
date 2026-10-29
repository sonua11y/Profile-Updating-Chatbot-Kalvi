
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_db
from app.db.models import Base, Course
from app.main import app

TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()



@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestingSessionLocal() as db:
            db.add(
                Course(
                    title="Test Course",
                    duration_months=6,
                    fee=1000,
                )
            )
            db.commit()

        test_client = TestClient(app)
        yield test_client
        test_client.close()
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)



def test_get_courses_returns_course_list(client):
    response = client.get("/profile/courses")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Test Course",
            "duration_months": 6,
            "fee": 1000.0,
        }
    ]
