from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, text, Float, exc, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, joinedload
import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
from data.example_data import inventory, store_locations

import data

load_dotenv(dotenv_path=Path(__file__).parent/".env")

Base = declarative_base()

username = os.getenv('PG_USERNAME')
password = os.getenv('PG_PASSWORD')


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    store_id = Column(String, unique=False)
    product_id = Column(String, unique=False)
    product = Column(String, unique=False)
    quantity = Column(Integer, unique=False)
    price = Column(Float, unique=False)



def initialize_database():
    """
    Initialize the database and return a session object.
    """
    inventory_engine = create_engine(f'postgresql://{username}:{password}@localhost:5432/{database_name}')
    
    Base.metadata.create_all(inventory_engine)
    Session = sessionmaker(bind=inventory_engine)
    session = Session()
    return session

def drop_table():
    Base.metadata.drop_all()


def insert_values_into_inventory(table, item: list, feature):
    try:
        session.add(table(
            **item
        ))
        session.commit()
    except exc.IntegrityError as e:
        session.rollback()
        print(f"IntegrityError: {e}")
    for item in session.query(table).all():
        print(getattr(item, feature))

if __name__=='__main__':
    database_name = 'store_inventory'
    session = initialize_database()
    for store in store_locations:
        for item in inventory:
            new_entry = item       
            new_entry['store_id'] = store['store_id']
            print(new_entry)
            session.add(Inventory(**item))
            session.commit()
            # insert_values_into_inventory(table=Inventory, item=new_entry, feature='store_id')
