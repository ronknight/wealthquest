import pytest
from unittest.mock import patch
from src.models import database

@patch("shutil.which", return_value="/usr/bin/termux-notification")
@patch("subprocess.run")
def test_test_notification_success(mock_run, mock_which, client):
    # This route doesn't require auth yet, but using client from conftest
    response = client.post("/api/v1/alerts/test")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    mock_run.assert_called_once()

@patch("shutil.which", return_value=None)
def test_test_notification_fail_no_api(mock_which, client):
    response = client.post("/api/v1/alerts/test")
    assert response.status_code == 500
    assert "termux-api not installed" in response.json()["detail"]

def test_alert_history(client, db, auth_headers):
    # Insert an alert directly into DB for history check
    alert = database.Alert(
        timestamp="2026-04-04T12:00:00",
        card_id=1,
        type="card_due",
        status="sent"
    )
    db.add(alert)
    db.commit()
    
    response = client.get("/api/v1/alerts/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["card_id"] == 1
    assert data[0]["status"] == "sent"
