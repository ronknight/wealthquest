import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.models.database import Base, get_db
from datetime import datetime, timedelta

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_card():
    due_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    response = client.post(
        "/api/v1/cards",
        json={"name": "Test Card", "due_date": due_date, "balance": 1000.0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Card"
    assert data["days_remaining"] == 5

def test_read_cards():
    due5 = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    due2 = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    client.post("/api/v1/cards", json={"name": "Card 5", "due_date": due5})
    client.post("/api/v1/cards", json={"name": "Card 2", "due_date": due2})
    
    response = client.get("/api/v1/cards")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Card 2" # Ordered by urgency

def test_update_threshold():
    post_response = client.post("/api/v1/cards", json={"name": "Threshold Card", "due_date": "2026-12-31"})
    card_id = post_response.json()["id"]
    
    response = client.put(f"/api/v1/cards/{card_id}/alert-threshold", json={"days": 7})
    assert response.status_code == 200
    assert response.json()["alert_threshold"] == 7

def test_update_card():
    post_response = client.post("/api/v1/cards", json={"name": "Old Card", "due_date": "2026-12-31"})
    card_id = post_response.json()["id"]
    
    response = client.put(
        f"/api/v1/cards/{card_id}",
        json={"name": "New Card", "due_date": "2027-01-01", "balance": 500.0}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Card"
    assert response.json()["balance"] == 500.0

def test_delete_card():
    post_response = client.post("/api/v1/cards", json={"name": "Delete Me", "due_date": "2026-12-31"})
    card_id = post_response.json()["id"]
    
    response = client.delete(f"/api/v1/cards/{card_id}")
    assert response.status_code == 204
    
    get_response = client.get("/api/v1/cards")
    assert len(get_response.json()) == 0
