from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///clients.db", echo=True)
Base= declarative_base()
Session = sessionmaker(bind=engine)

session = Session()

class Client(Base):

    __tablename__= "Client"

    id= Column(Integer, primary_key = True)

    name = Column(String)
    email= Column(String)
    bank= Column(String)

Base.metadata.create_all(engine)



person1 = session.get(Client,name="Sara")
session.commit()

print(person1)

