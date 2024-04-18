from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Database configuration
database = {
    "username": 'root',
    "password": 'root',
    "database_name": 'Oriens',
    "hostname": 'localhost'
}
DATABASE_URL = f"mysql+mysqlconnector://{database['username']}:{database['password']}@{database['hostname']}/{database['database_name']}"

# Create the database engine and connect
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()
# Define the Seller class
class Seller(Base):
    __tablename__ = 'seller'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    client_id = Column(Integer, nullable=False)
    licence_key = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    pos_id = Column(Integer, nullable=False)
    tenant_id = Column(String(255))
    number_of_licence = Column(Integer)
    whether_free = Column(String(255), nullable=False)
    trial_end_date = Column(Date)


Base.metadata.create_all(engine)
# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
