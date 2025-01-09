# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from app.models import Cause




# Configure a test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency override for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables for the test database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Test client instance
@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# Prepopulate test data
@pytest.fixture(scope="module")
def test_cause():
    db = TestingSessionLocal()
    new_cause = Cause(
        title = "Social Causes",
        description = "A cause that is open to contributions",
        image_url = "https://image.url"
    )
    db.add(new_cause)
    db.commit()
    db.refresh(new_cause)
    
    return new_cause

@pytest.fixture(scope="module")
def test_cause_data():
    cause_data  = {
    "title" : "Social Cause",
    "description" : "A cause that is open to contributions",
    "image_url" : "https://image.url"
    }
    return cause_data

@pytest.fixture(scope="module")
def test_update_cause_data():
    cause_data  = {
    "title" : "New Social Cause",
    "description" : "A cause that is not totally open to contributions",
    "image_url" : "https://new-image.url"
    }
    return cause_data

@pytest.fixture(scope="module")
def test_contribution_data(): 
    new_contribution = {
        "name" : "Contributor",
        "email" : "contributor@email.com",
        "amount" : "1000000"
    }
    return new_contribution