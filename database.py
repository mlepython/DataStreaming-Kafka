# TODO need to create a connection to a database. Mysql, postgress, sqlite, azure, ibm
# TODO need dimension tables for product, location, customer, date
# create the dimensions before hand? allow for new values to be inserted into table. this will require a check to see if value already in table
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, text, Float
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    # Add other fields as needed

class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    address = Column(String, unique=False)
    city = Column(String, unique=False)
    province = Column(String, unique=False)
    postal_code = Column(String, unique=False)
    

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    product = Column(String, unique=False)
    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)

class PaymentOptions(Base):
    __tablename__ = 'payment_options'
    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)
    description = Column(String, unique=False)

class TaxRate(Base):
    __tablename__ = "tax_rate"
    id = Column(Integer, primary_key=True)
    province = Column(String, unique=False)
    rate = Column(Float, unique=False)

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=False)
    email = Column(String, unique=False)

username = 'postgres'
password = 'sqlpassword'
database_name = 'SalesData'
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/{database_name}')
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)

# all_transactions = session.query(Transaction).all()

# with engine.connect() as connection:
#     result = connection.execute(text("SELECT * FROM actor"))

#     for row in result:
#         print(f"Transaction ID: {row}")
