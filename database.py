# TODO need to create a connection to a database. Mysql, postgress, sqlite, azure, ibm
# TODO need dimension tables for product, location, customer, date
# create the dimensions before hand? allow for new values to be inserted into table. this will require a check to see if value already in table
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, text, Float, exc, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
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
    # date_id
    customer_id = Column(String, ForeignKey('customer.customer_id'))
    customer = relationship('Customer', back_populates='transactions')
    store_id = Column(String, ForeignKey('store.store_id'))
    store = relationship('Store', back_populates='transactions')
    payment_id = Column(Integer, ForeignKey('payment_options.id'))
    payment_option = relationship('PaymentOptions', back_populates='transactions')
    items_purchased = relationship('ItemsPurchased', back_populates='transaction')    

class ItemsPurchased(Base):
    __tablename__ = 'items_purchased'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, ForeignKey('transactions.transaction_id'))

    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)
    product_id = Column(String, ForeignKey('inventory.product_id'))
    product = relationship('Inventory', back_populates='item_purchased')
    transaction = relationship('Transaction', back_populates='items_purchased')

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True)
    product = Column(String, unique=False)
    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)
    item_purchased = relationship('ItemsPurchased', back_populates='product')

class Date(Base):
    __tablename__ = 'date'
    # date dimension table
    id = Column(Integer, primary_key=True)

class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    store_id = Column(String, unique=True)
    name = Column(String, unique=False)
    address = Column(String, unique=False)
    city = Column(String, unique=False)
    province = Column(String, unique=False)
    postal_code = Column(String, unique=False)
    transactions = relationship('Transaction', back_populates='store')
    
class PaymentOptions(Base):
    __tablename__ = 'payment_options'
    id = Column(Integer, primary_key=True)
    payment_id = Column(String, unique=True)
    type = Column(String, unique=True)
    description = Column(String, unique=False)
    transactions = relationship('Transaction', back_populates='payment_option')

class TaxRate(Base):
    __tablename__ = "tax_rate"
    id = Column(Integer, primary_key=True)
    province = Column(String, unique=True)
    rate = Column(Float, unique=False)

class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    customer_id = Column(String, unique=True)
    first_name = Column(String, unique=False)
    last_name = Column(String, unique=False)
    email = Column(String, unique=False)
    street = Column(String, unique=False)
    city = Column(String, unique=False)
    province = Column(String, unique=False)
    postal_code = Column(String, unique=False)
    transactions = relationship('Transaction', back_populates='customer')

def update_transaction_table(data):
    session.add(Transaction(
        transaction_id=data['transaction_id'],
        timestamp=data['transaction_date'],
        subtotal=data['subtotal'],
        tax=data['tax'],
        total=data['total'],
        customer_id=data['customer_id'],
        store_id=data['location']['store_id']

    ))
    session.commit()

def updated_items_purchased_table(data):
    for item in data['items']:
        inventory_item = session.query(Inventory).filter_by(product=item['item']).first()
        if inventory_item:
            product_id = inventory_item.product_id
        else:
            print('Product Not Found')
            product_id = None
        session.add(ItemsPurchased(
            transaction_id=data['transaction_id'],
            quantity=item['quantity'],
            price=item['price'],
            product_id=product_id,
        ))
    session.commit()
    

engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/{database_name}')
# Base.metadata.drop_all(engine)
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

        all_rates = session.query(TaxRate).all()
        for tax_rate in all_rates:
            print(f"Province: {tax_rate.province}, Rate: {tax_rate.rate}")
    def update_database(table, data: list, feature):
        try:
            for item in data:
                session.add(table(
                    **item
                ))
            session.commit()
        except exc.IntegrityError as e:
            session.rollback()
            print(f"IntegrityError: {e}")
        for item in session.query(table).all():
            print(getattr(item, feature))

    update_database(table=Inventory, data=inventory, feature='product_id')
    update_database(table=Customer, data=canadian_customers, feature='customer_id')
    update_database(table=PaymentOptions, data=payment_options, feature='type')
    update_database(table=Store, data=store_locations, feature='store_id')
    # update_transaction_table(data=pos_example)
    # update_transaction_table(data=pos_example_2)
    result = session.query(Transaction).options(joinedload(Transaction.customer)).first()
    for attr, value in result.__dict__.items():
        print(f"{attr}: {value}")
    print("\n")
    updated_items_purchased_table(data=pos_example_2)



