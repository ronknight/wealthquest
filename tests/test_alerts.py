import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import app
from src.models import database
from src.models.database import Base, get_db
from unittest.mock import patch, MagicMock

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

@patch("shutil.which", return_value="/usr/bin/termux-notification")
@patch("subprocess.run")
def test_test_notification_success(mock_run, mock_which):
    response = client.post("/api/v1/alerts/test")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_run.assert_called_once()

@patch("shutil.which", return_value=None)
def test_test_notification_fail_no_api(mock_which):
    response = client.post("/api/v1/alerts/test")
    assert response.status_code == 500
    assert "termux-api not installed" in response.json()["detail"]

def test_alert_history():
    # Insert an alert directly into DB for history check
    db = TestingSessionLocal()
    # Need to have a card to reference if we want to be strict, but alert model just takes card_id
    alert = database.Alert(
        timestamp="2026-04-04T12:00:00",
        card_id=1,
        type="card_due",
        status="sent"
    )
    db.add(alert)
    db.commit()
    
    response = client.get("/api/v1/alerts/history")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["card_id"] == 1
    assert data[0]["status"] == "sent"
