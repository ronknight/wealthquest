import pytest
from fastapi.testclient import TestClient
from src.main import app

def test_register_and_login_long_password(client):
    """Verify that a user can register and login with a password longer than 72 characters."""
    username = "long_pass_user"
    long_password = "a" * 80
    
    # Register
    register_response = client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": long_password}
    )
    assert register_response.status_code == 200
    assert register_response.json()["username"] == username
    
    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": long_password}
    )
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def test_login_wrong_password_long(client):
    """Verify that a wrong long password still returns 401, not 500."""
    username = "normal_user"
    password = "password123"
    
    # Register
    client.post(
        "/api/v1/auth/register",
        json={"username": username, "password": password}
    )
    
    # Login with wrong long password
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": "b" * 80}
    )
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Incorrect username or password"
