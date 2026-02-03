import pytest
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, engine, Session
from models import Base, Client
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def client():
    app.config.from_object(TestConfig)
    
    # Use an in-memory database for testing
    # Note: Since app.py uses a global engine, we might need a way to override it 
    # or just use a separate test db file if the architecture makes dependency injection hard.
    # Given the structure, we will update the engine URL for the session maker if possible
    # or just rely on a test_db file.
    
    # For this simple setup, let's just use a separate test.db
    app.config['DB_URI'] = "sqlite:///test_clients.db"
    
    # Create tables
    from sqlalchemy import create_engine
    test_engine = create_engine(app.config['DB_URI'])
    Base.metadata.create_all(test_engine)
    
    # Patch the session to use our test engine
    # In a real app we'd use dependency injection, but here we can try to patch or just use the file
    # app.py's Session is bound to 'engine'.
    
    with app.test_client() as client:
        with app.app_context():
            yield client
    
    # Cleanup
    Base.metadata.drop_all(test_engine)
    if os.path.exists("test_clients.db"):
        os.remove("test_clients.db")

@pytest.fixture
def init_database():
    # Helper to setup initial data
    yield 
