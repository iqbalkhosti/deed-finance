# from sqlalchemy import create_engine, ForeignKey, Column, Integer, String,text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# engine = create_engine("sqlite:///clients.db", echo=True)
# DbBase= declarative_base()
# Session = sessionmaker(bind=engine)

# session = Session()

# class Client(DbBase):

#     __tablename__= "client"

#     id= Column(Integer, primary_key = True)

#     first_name = Column(String(100))
#     email= Column(String(100))
#     bank= Column(String(100), unique=True)
#     password = Column(String(200))



# DbBase.metadata.create_all(engine)



# session.execute.text('ALTER TABLE Client ADD COLUMN password TEXT')

# session.commit()


