"""
Centralized database configuration for Deed Finance.
Handles SQLite (local dev) and PostgreSQL (Supabase production) transparently.
"""
import os
import ssl
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

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
        # Use pg8000 driver (pure Python — no native C library issues on Vercel)
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+pg8000://", 1)
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
    On Vercel, uses NullPool (no persistent connections — each request opens/closes its own).
    """
    if database_url is None:
        database_url = get_database_url()

    engine_kwargs = {"echo": False}

    if is_sqlite(database_url):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    else:
        # pg8000 needs an ssl_context for Supabase (which requires SSL)
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        engine_kwargs["connect_args"] = {"ssl_context": ssl_ctx}

        is_vercel = os.environ.get("VERCEL") == "1"
        if is_vercel:
            # Serverless: NullPool is safest — no stale connections across invocations
            engine_kwargs["poolclass"] = NullPool
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
