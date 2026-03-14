"""
One-time script to create all tables in the Supabase PostgreSQL database.
Usage: DATABASE_URL="postgresql+pg8000://..." python init_db.py
"""
from db import engine, get_database_url
from models import DbBase

if __name__ == "__main__":
    db_url = get_database_url()
    print(f"Database URL: {db_url[:40]}...")
    print(f"Tables to create: {list(DbBase.metadata.tables.keys())}")

    DbBase.metadata.create_all(engine)

    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    existing = inspector.get_table_names()
    print(f"Tables now in database: {existing}")
    print("Done!")
