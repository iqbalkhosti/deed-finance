# tempCodeRunnerFile.py

# 1) import the SQLAlchemy Session class
from sqlalchemy.orm import Session

# 2) import your engine
from fin_database import engine

# 3) import your model
def main():
    # make sure the table exists
    # (if you’ve been using Base.metadata.create_all(engine) elsewhere,
    # you can skip this—but it doesn’t hurt)
    # from models import Base
    # Base.metadata.create_all(engine)

    # open a Session and insert a dummy record
    with Session(bind=engine) as session:
        dummy = Client(
            first_name="Temp",
            surname="Runner",
            email="temp.runner@example.com",
            password="notarealpassword"
        )
        session.add(dummy)
        session.commit()

        print(f"Inserted dummy client with id = {dummy.id}")

if __name__ == "__main__":
    main()

