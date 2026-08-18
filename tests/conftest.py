import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app
from app.models.opportunity import Opportunity


TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def sample_opportunities(db_session):
    opportunities = [
        Opportunity(
            title="Remote Software Engineer",
            company="Test Company",
            location="Berlin",
            city="Berlin",
            country="Germany",
            remote=True,
            url="https://example.com/remote-engineer",
            source="Test",
        ),
        Opportunity(
            title="Backend Engineer",
            company="Test Company",
            location="Munich",
            city="Munich",
            country="Germany",
            remote=False,
            url="https://example.com/backend-engineer",
            source="Test",
        ),
        Opportunity(
            title="Remote Data Analyst",
            company="Another Company",
            location="London",
            city="London",
            country="United Kingdom",
            remote=True,
            url="https://example.com/data-analyst",
            source="Test",
        ),
    ]

    db_session.add_all(opportunities)
    db_session.commit()

    return opportunities