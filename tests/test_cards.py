import pytest
from datetime import datetime, timedelta

def test_create_card(client, auth_headers):
    due_date = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    response = client.post(
        "/api/v1/cards",
        json={"name": "Test Card", "due_date": due_date, "balance": 1000.0},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Card"
    assert data["days_remaining"] == 5

def test_read_cards(client, auth_headers):
    due5 = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
    due2 = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    client.post("/api/v1/cards", json={"name": "Card 5", "due_date": due5}, headers=auth_headers)
    client.post("/api/v1/cards", json={"name": "Card 2", "due_date": due2}, headers=auth_headers)
    
    response = client.get("/api/v1/cards", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Card 2" # Ordered by urgency

def test_update_threshold(client, auth_headers):
    post_response = client.post("/api/v1/cards", json={"name": "Threshold Card", "due_date": "2026-12-31"}, headers=auth_headers)
    card_id = post_response.json()["id"]
    
    response = client.put(f"/api/v1/cards/{card_id}/alert-threshold", json={"days": 7}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["alert_threshold"] == 7

def test_update_card(client, auth_headers):
    post_response = client.post("/api/v1/cards", json={"name": "Old Card", "due_date": "2026-12-31"}, headers=auth_headers)
    card_id = post_response.json()["id"]
    
    response = client.put(
        f"/api/v1/cards/{card_id}",
        json={"name": "New Card", "due_date": "2027-01-01", "balance": 500.0},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["name"] == "New Card"
    assert response.json()["balance"] == 500.0

def test_delete_card(client, auth_headers):
    post_response = client.post("/api/v1/cards", json={"name": "Delete Me", "due_date": "2026-12-31"}, headers=auth_headers)
    card_id = post_response.json()["id"]
    
    response = client.delete(f"/api/v1/cards/{card_id}", headers=auth_headers)
    assert response.status_code == 204
    
    get_response = client.get("/api/v1/cards", headers=auth_headers)
    assert len(get_response.json()) == 0
