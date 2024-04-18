from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from ...database.connection1 import engine
Base = declarative_base()
# Define the Seller class
class Seller(Base):
    __tablename__ = 'seller'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    client_id = Column(Integer, nullable=False)
    licence_key = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    pos_id = Column(Integer, nullable=False)
    tenant_id = Column(String)
    number_of_licence = Column(Integer)
    whether_free = Column(String, nullable=False)
    trial_end_date = Column(Date)


Base.metadata.create_all(engine)

