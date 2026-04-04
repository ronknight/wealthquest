import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.models.database import Base, get_db

# Test database setup - Use in-memory for tests
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

def test_create_payment():
    response = client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 100.0, "date": "2026-04-04", "source": "Test Source", "tax_flag": 0}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 100.0
    assert data["source"] == "Test Source"
    assert "id" in data

def test_read_payments():
    client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 100.0, "date": "2026-04-04", "source": "Source 1", "tax_flag": 0}
    )
    client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 200.0, "date": "2026-04-05", "source": "Source 2", "tax_flag": 0}
    )
    response = client.get("/api/v1/side-hustle/payments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["amount"] == 200.0 # Ordered by date desc

def test_update_payment():
    post_response = client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 100.0, "date": "2026-04-04", "source": "Old Source", "tax_flag": 0}
    )
    payment_id = post_response.json()["id"]
    
    response = client.put(
        f"/api/v1/side-hustle/payments/{payment_id}",
        json={"amount": 150.0, "date": "2026-04-04", "source": "New Source", "tax_flag": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 150.0
    assert data["source"] == "New Source"
    assert data["tax_flag"] == 1

def test_delete_payment():
    post_response = client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 100.0, "date": "2026-04-04", "source": "To Delete", "tax_flag": 0}
    )
    payment_id = post_response.json()["id"]
    
    response = client.delete(f"/api/v1/side-hustle/payments/{payment_id}")
    assert response.status_code == 204
    
    get_response = client.get("/api/v1/side-hustle/payments")
    assert len(get_response.json()) == 0

def test_net_cash():
    client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 100.0, "date": "2026-04-04", "source": "Net 1", "tax_flag": 0}
    )
    client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 200.0, "date": "2026-04-05", "source": "Taxable", "tax_flag": 1}
    )
    client.post(
        "/api/v1/side-hustle/payments",
        json={"amount": 50.0, "date": "2026-04-06", "source": "Net 2", "tax_flag": 0}
    )
    
    response = client.get("/api/v1/side-hustle/net-cash")
    assert response.status_code == 200
    assert response.json()["net_cash"] == 150.0
