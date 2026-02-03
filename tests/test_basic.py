import pytest
from models import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def test_index(client):
    """Test landing page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Stop Paying for Subscriptions" in response.data

def test_signup_page(client):
    """Test signup page loads."""
    response = client.get('/signup')
    assert response.status_code == 200
    assert b"Sign Up" in response.data

def test_login_page(client):
    """Test login page loads."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Log In" in response.data

# Note: More comprehensive tests would involve mocking the DB session 
# or handling the global Session object in app.py more gracefully for tests.
