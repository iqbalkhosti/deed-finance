import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database
    # Using relative path for SQLite to work in both dev and likely prod simple cases
    # For production, this should likely be overridden by an env var
    DB_NAME = "clients.db"
    DB_URI = os.environ.get("DATABASE_URL", f"sqlite:///{DB_NAME}")
    
    # Email / Dev Mode
    DEV_MODE = os.environ.get("DEV_MODE", "true").lower() == "true"
