from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///clients.db", echo=True)
Base= declarative_base()
Session = sessionmaker(bind=engine)

session = Session()

class Client(Base):
    __tablename__ = "Client"
    id         = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    surname    = Column(String(100))         # ← add this
    email      = Column(String(100))
    # bank       = Column(String(100), unique=True)
    password   = Column(String(200))

Base.metadata.create_all(engine)


# the following line is for inserting any sql query to the database.

# with engine.connect() as conn:
#     conn.execute(
#         text("ALTER TABLE Client ADD COLUMN surname VARCHAR(100)")
#         )
#     conn.commit()

# <---- THE CODE BELOW IS CHANGED AS WE ARE SWITCHING FROM A SERVER BASED DATABASE TO A LOCAL DATABASE ----> #



# from sqlalchemy import create_engine
# from dotenv import load_dotenv
# import os

# #creating the connection between the mysql and code out here

# load_dotenv()

# DB_URL = os.getenv("DATABASE_CONNECTION_STRING")

# if not DB_URL:
#     raise ValueError("The code db url is not working")

# engine = create_engine(DB_URL)

# # with engine.connect() as conn:
# #     result = conn.execute(text("SELECT * FROM user"))
# #     result_all = result.all()

# #     # here creating a dictionary of the sqlalchemy objects

# #     result_dicts = [row._mapping for row in result_all]
    
# #     print(result_dicts)
