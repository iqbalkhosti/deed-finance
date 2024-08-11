from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#creating the connection between the mysql and code out here

load_dotenv()

DB_URL = os.getenv("DATABASE_CONNECTION_STRING")

if not DB_URL:
    raise ValueError("The code db url is not working")

engine = create_engine(DB_URL)

# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM user"))
#     result_all = result.all()

#     # here creating a dictionary of the sqlalchemy objects

#     result_dicts = [row._mapping for row in result_all]
    
#     print(result_dicts)