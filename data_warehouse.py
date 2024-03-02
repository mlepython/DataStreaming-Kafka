from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, text, Float, exc, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
from data.example_data import *

load_dotenv(dotenv_path=Path(__file__).parent/".env")

Base = declarative_base()

username = os.getenv('PG_USERNAME')
password = os.getenv('PG_PASSWORD')

database_name = 'salesdata'


class Transaction(Base):
    __tablename__ = 'transactions_FACT'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, unique=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    subtotal = Column(Float, unique=False)
    tax = Column(Float, unique=False)
    total = Column(Float, unique=False)

    customer_id = Column(String, ForeignKey('customer_DIM.customer_id'))
    store_id = Column(String, ForeignKey('store_DIM.store_id'))
    payment_id = Column(Integer, ForeignKey('payment_options_DIM.id'))
    date_id = Column(Integer, ForeignKey('date_DIM.id'))

    date = relationship('Date', back_populates='transaction')
    customer = relationship('Customer', back_populates='transactions')
    store = relationship('Store', back_populates='transactions')
    payment_option = relationship('PaymentOptions', back_populates='transaction')
    items_purchased = relationship('ItemsPurchased', back_populates='transaction')

class ItemsPurchased(Base):
    __tablename__ = 'items_purchased_FACT'
    id = Column(Integer, primary_key=True)
    transaction_id = Column(String, ForeignKey('transactions_FACT.transaction_id'))
    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)
    product_id = Column(String, ForeignKey('inventory.product_id'))
    product = relationship('Inventory', back_populates='item_purchased')
    transaction = relationship('Transaction', back_populates='items_purchased')

# TODO need to create an inventory table for each store? or just include the store_id into the table?
class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    product_id = Column(String, unique=True)
    product = Column(String, unique=False)
    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)
    item_purchased = relationship('ItemsPurchased', back_populates='product')

class Date(Base):
    __tablename__ = 'date_DIM'
    # date dimension table
    id = Column(Integer, primary_key=True)
    day = Column(Integer, unique=False)
    weekday_name = Column(String, unique=False)
    weekday = Column(Integer, unique=False)
    month = Column(Integer, unique=False)
    month_name = Column(String, unique=False)
    quarter = Column(Integer, unique=False)
    quarter_name = Column(String, unique=False)
    year = Column(Integer, unique=False)
    transaction = relationship('Transaction', back_populates='date')

class Store(Base):
    __tablename__ = 'store_DIM'
    id = Column(Integer, primary_key=True)
    store_id = Column(String, unique=True)
    name = Column(String, unique=False)
    address = Column(String, unique=False)
    city = Column(String, unique=False)
    province = Column(String, unique=False)
    postal_code = Column(String, unique=False)
    transactions = relationship('Transaction', back_populates='store')
    
class PaymentOptions(Base):
    __tablename__ = 'payment_options_DIM'
    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)
    description = Column(String, unique=False)
    transaction = relationship('Transaction', back_populates='payment_option')

class TaxRate(Base):
    __tablename__ = "tax_rate"
    id = Column(Integer, primary_key=True)
    province = Column(String, unique=True)
    rate = Column(Float, unique=False)

class Customer(Base):
    __tablename__ = 'customer_DIM'
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

def update_customer_table(data):
    # check to see if customer already in table
    customer_entry = session.query(Customer).filter_by(customer_id=data['customer_id']).first()
    if not customer_entry:
        session.add(Customer(**data))
        session.commit()
        print("New customer added to warehouse")

def update_store_table(data):
    # check to see if store location already in table
    store_entry = session.query(Store).filter_by(store_id=data['store_id']).first()
    if not store_entry:
        session.add(Store(
            **data
        ))
        session.commit()
        print("New store added to warehouse")

def update_transaction_table(data, customer_id, store_id):
    transaction_entry = session.query(Transaction).filter_by(transaction_id=data['transaction_id']).first()
    if not transaction_entry:
        # get payment type id
        payment_entry = session.query(PaymentOptions).filter_by(type=data['payment_type']).first()
        if payment_entry:
            payment_id = payment_entry.id
        else:
            payment_id = None
        # get date id from date dim table
        datetime_object = datetime.datetime.strptime(data['transaction_date'], "%Y-%m-%d %H:%M:%S")
        date_entry = session.query(Date).filter_by(day=datetime_object.day,
                                                   month=datetime_object.month,
                                                   year=datetime_object.year).first()
        if date_entry:
            date_id = date_entry.id
        else:
            date_id = None
        session.add(Transaction(
                transaction_id=data['transaction_id'],
                timestamp=data['transaction_date'],
                subtotal=data['subtotal'],
                tax=data['tax'],
                total=data['total'],
                customer_id=customer_id,
                store_id=store_id,
                payment_id=payment_id,
                date_id=date_id
            ))
        session.commit()

def update_date_table(data):
    datetime_object = datetime.datetime.strptime(data['transaction_date'], "%Y-%m-%d %H:%M:%S")
    date_data = {
        "day": datetime_object.day,
        "weekday_name": datetime_object.strftime("%A"),
        "weekday": datetime_object.weekday(),
        "month": datetime_object.month,
        "month_name": datetime_object.strftime("%B"),
        "quarter": (datetime_object.month-1) // 3 + 1,
        "quarter_name": f'Q{(datetime_object.month-1) // 3 + 1}',
        "year": datetime_object.year
    }
    # check if date is already in date dim table. if not add a new record
    date_entry = session.query(Date).filter_by(
        day=date_data['day'], month=date_data['month'], year=date_data['year']
    ).first()
    if not date_entry:
        # add new entry to date table if record does not exist
        session.add(Date(**date_data))
        session.commit()

def updated_items_purchased_table(data, transaction_id):
    for item in data:
        inventory_item = session.query(Inventory).filter_by(product=item['item']).first()
        if inventory_item:
            product_id = inventory_item.product_id
        else:
            print('Product Not Found')
            product_id = None
        session.add(ItemsPurchased(
            transaction_id=transaction_id,
            quantity=item['quantity'],
            price=item['price'],
            product_id=product_id,
        ))
    session.commit()
    print('New item added to table')
    

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
    
    def insert_values_into_database(table, data: list, feature):
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

    insert_values_into_database(table=Inventory, data=inventory, feature='product_id')
    insert_values_into_database(table=Customer, data=canadian_customers, feature='customer_id')
    insert_values_into_database(table=PaymentOptions, data=payment_options, feature='type')
    insert_values_into_database(table=Store, data=store_locations, feature='store_id')

    
    # update_transaction_table(data=pos_example_3)
    # update_date_table(data=pos_example_3)
    
    # update_transaction_table(data=pos_example_2)
    update_date_table(data=pos_example_2)
    # result = session.query(Transaction).options(joinedload(Transaction.customer)).first()
    # for attr, value in result.__dict__.items():
    #     print(f"{attr}: {value}")
    # print("\n")
    # updated_items_purchased_table(data=pos_example_2)
    



