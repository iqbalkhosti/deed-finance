"""
Centralized database configuration for Deed Finance.
Handles SQLite (local dev) and PostgreSQL (Supabase production) transparently.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_database_url():
    """
    Determine the database URL.
    Priority:
    1. DATABASE_URL environment variable (Supabase PostgreSQL in production)
    2. Local SQLite file as fallback for development
    """
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        # Supabase/Heroku sometimes provide postgres:// which SQLAlchemy 1.4+ rejects
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    # Local SQLite fallback
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "clients.db")
    return f"sqlite:///{db_path}"


def is_sqlite(url=None):
    """Check if the database URL is SQLite."""
    if url is None:
        url = get_database_url()
    return url.startswith("sqlite")


def create_db_engine(database_url=None):
    """
    Create a SQLAlchemy engine with appropriate settings for the database type.
    Uses smaller connection pool on Vercel/serverless to avoid exhausting DB connections.
    """
    if database_url is None:
        database_url = get_database_url()

    engine_kwargs = {"echo": False}

    if is_sqlite(database_url):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    else:
        # Serverless (Vercel): each function instance gets its own pool - keep it small
        is_vercel = os.environ.get("VERCEL") == "1"
        if is_vercel:
            engine_kwargs["pool_size"] = 1
            engine_kwargs["max_overflow"] = 2
        else:
            engine_kwargs["pool_size"] = 5
            engine_kwargs["max_overflow"] = 10
        engine_kwargs["pool_timeout"] = 30
        engine_kwargs["pool_recycle"] = 1800
        engine_kwargs["pool_pre_ping"] = True

    return create_engine(database_url, **engine_kwargs)


# Module-level defaults
engine = create_db_engine()
Session = sessionmaker(bind=engine)
