import pytest
import asyncio
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from src.main import alert_scheduler
from src.models import database
from datetime import datetime, timedelta

@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    database.Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSessionLocal

@pytest.mark.asyncio
@patch("src.services.alerts.process_card_alert")
@patch("asyncio.sleep", side_effect=asyncio.CancelledError)
async def test_scheduler_triggers_alert(mock_sleep, mock_process, test_db):
    # Add a card that needs alert
    db = test_db()
    due_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    card = database.Card(name="Scheduler Card", due_date=due_date, alert_threshold=3)
    db.add(card)
    db.commit()
    
    # Patch SessionLocal used in alert_scheduler
    with patch("src.main.SessionLocal", return_value=db):
        try:
            await alert_scheduler()
        except asyncio.CancelledError:
            pass
    
    mock_process.assert_called_once()
    db.close()

@pytest.mark.asyncio
@patch("src.services.alerts.process_card_alert")
@patch("asyncio.sleep", side_effect=asyncio.CancelledError)
async def test_scheduler_deduplication(mock_sleep, mock_process, test_db):
    db = test_db()
    due_date = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    card = database.Card(name="Dedupe Card", due_date=due_date, alert_threshold=3)
    db.add(card)
    db.commit()
    
    # Add an alert sent today
    alert = database.Alert(
        timestamp=datetime.now().isoformat(),
        card_id=card.id,
        type="card_due",
        status="sent"
    )
    db.add(alert)
    db.commit()
    
    # Patch SessionLocal used in alert_scheduler
    with patch("src.main.SessionLocal", return_value=db):
        try:
            await alert_scheduler()
        except asyncio.CancelledError:
            pass
    
    # Should NOT trigger alert because one was sent today
    mock_process.assert_not_called()
    db.close()
