# TODO create a simulator for point of sale data from a grocery store
# item, price per item, quantity, date of purchase, cash/card, total amount, location (name of store, address, province)
# customer id (new or current customer?)
# will need to store the data into a Fact table and Dimension tables. Send the simulated data as a json.
# include taxes, they will change from province to province
# TODO download apache kafka and install
import random
import time
import uuid
import datetime
from example_data import *
from database import engine, TaxRate, session
# from kafka import KafkaProducer
# producer = KafkaProducer(bootstrap_servers='localhost:9092')

num_items = len(items)
num_payment_types = len(payment_options)
num_stores = len(store_locations)

items_purchased = random.sample(items, k=random.randint(3,num_items))
payment_type = random.choice(payment_options)
store = random.choice(store_locations)

# based on store provice get the correct tax rate
try:
    # tax_rate = canadian_tax_rates[store['province']]
    province = store['province']
    tax_rate = session.query(TaxRate).filter_by(province=province).first()
    tax_rate = tax_rate.rate
    print(f"Province: {province}\nTax Rate: {tax_rate}")
except KeyError:
    print("Province not found. tax rate sent to 0.1")
    tax_rate = 0.1

# generate a random id for transaction id
transaction_id = uuid.uuid4()
# get the current date and time for transaction date
transaction_date = datetime.datetime.utcnow()

# calculte the subtotal and total for the bill and tax
def bill(items: list, tax_rate: float):
    subtotal = 0
    for item in items:
        quantity = random.randint(1,3)
        subtotal += item['price']*quantity
    tax = subtotal*tax_rate
    total = subtotal + tax
    return {"subtotal": round(subtotal, 2), "tax": round(tax, 2), "total": round(total, 2)}

print(bill(items=items_purchased, tax_rate=tax_rate))
# TODO need customer id 

# TODO will need to access the databases for customer, item, payment options, etc...


