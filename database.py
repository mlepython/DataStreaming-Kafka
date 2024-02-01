# TODO need to create a connection to a database. Mysql, postgress, sqlite, azure, ibm
# TODO need dimension tables for product, location, customer, date
# create the dimensions before hand? allow for new values to be inserted into table. this will require a check to see if value already in table
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, text, Float, exc
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime
from dotenv import load_dotenv
import os
from example_data import *

load_dotenv()

Base = declarative_base()

username = os.getenv('PG_USERNAME')
password = os.getenv('PG_PASSWORD')

database_name = 'SalesData'


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    subtotal = Column(Float, unique=False)
    tax = Column(Float, unique=False)
    total = Column(Float, unique=False)
    # TODO items, customer info, cost, payment method, store info
    # these are foreign keys
    # customer_id
    # store_id
    # payment_id
    # item_id?
# TODO have a database to handle the items purchased for each transaction?
class ItemsPurchased(Base):
    __tablename__ = 'items_purchased'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=False)
    item_id = Column(String, unique=False)
    quantity = Column(Integer, unique=False)

class Date(Base):
    __tablename__ = 'date'
    # date dimension table
    id = Column(Integer, primary_key=True)
class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    store_id = Column(String, unique=False)
    name = Column(String, unique=False)
    address = Column(String, unique=False)
    city = Column(String, unique=False)
    province = Column(String, unique=False)
    postal_code = Column(String, unique=False)
    

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True)
    product = Column(String, unique=False)
    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)

class PaymentOptions(Base):
    __tablename__ = 'payment_options'
    id = Column(Integer, primary_key=True)
    payment_id = Column(String, unique=True)
    type = Column(String, unique=True)
    description = Column(String, unique=False)

class TaxRate(Base):
    __tablename__ = "tax_rate"
    id = Column(Integer, primary_key=True)
    province = Column(String, unique=True)
    rate = Column(Float, unique=False)

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String, unique=False)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    email = Column(String, unique=False)
    street = Column(String, unique=False)
    city = Column(String, unique=False)
    province = Column(String, unique=False)
    postal_code = Column(String, unique=False)
    
engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/{database_name}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

if __name__=='__main__':
    try:
        for province, rate in canadian_tax_rates.items():
            session.add(TaxRate(province=province, rate=rate))
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e}")
    else:
        print("Successfully added user with unique email.")
    all_rates = session.query(TaxRate).all()
    for tax_rate in all_rates:
        print(f"Province: {tax_rate.province}, Rate: {tax_rate.rate}")
    
    try:
        for province, rate in canadian_tax_rates.items():
            session.add(TaxRate(province=province, rate=rate))
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e}")
    else:
        print("Successfully added user with unique email.")
    all_rates = session.query(TaxRate).all()
    for tax_rate in all_rates:
        print(f"Province: {tax_rate.province}, Rate: {tax_rate.rate}")
    
    # for province, rate in canadian_tax_rates.items():
    #     session.add(TaxRate(province=province, rate=rate))
    #     session.commit()
    # all_rates = session.query(TaxRate).all()
    # for tax_rate in all_rates:
    #     print(f"Province: {tax_rate.province}, Rate: {tax_rate.rate}")


