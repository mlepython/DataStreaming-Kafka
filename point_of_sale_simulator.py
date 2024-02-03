import random
import json
import time
import uuid
import datetime
from example_data import *
from database import engine, TaxRate, session
# from kafka import KafkaProducer
# producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
# producer = KafkaProducer(bootstrap_servers='localhost:9092')

NUM_ITEMS = len(items)
NUM_PAYMENT_TYPES = len(payment_options)
NUM_STORES = len(store_locations)
TOPIC = "PointOfSale"

def bill(items: list, tax_rate: float):
    subtotal = 0
    for item in items:
        subtotal += item['total_price']
    tax = subtotal*tax_rate
    total = subtotal + tax
    return {"subtotal": round(subtotal, 2), "tax": round(tax, 2), "total": round(total, 2)}

def cutomer_id_generator():
    # for new customers not in customer database
    id = f'CUST{randint(0,9)}{randint(0,9)}{randint(0,9)}'
    return id

def product_id_generator():
    # for new products not in database
    id = f'PROD{randint(0,9)}{randint(0,9)}{randint(0,9)}'
    return id

def transaction_generator():
    # generate a random id for transaction id
    transaction_id = str(uuid.uuid4())
    # get the current date and time for transaction date
    transaction_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # randomly select items, payment type, store, and customer id for a given transaction
    items_purchased = random.sample(items, k=random.randint(3,NUM_ITEMS))
    payment_type = random.choice(payment_options)
    store = random.choice(store_locations)
    customer = random.choice(canadian_customers)

    # based on store provice get the correct tax rate
    try:
        province = store['province']
        tax_rate = session.query(TaxRate).filter_by(province=province).first()
        tax_rate = tax_rate.rate
        print(f"Province: {province}\nTax Rate: {tax_rate}")
    except KeyError:
        print("Province not found. tax rate sent to 0.1")
        tax_rate = 0.1

    # randomly generate the quantity
    def item_quantity(items: list):
        updated_items = []
        for item in items:
            quantity = random.randint(1,3)
            item['quantity'] = quantity
            item['total_price'] = round(item['price']*quantity, 2)
            updated_items.append(item)
        return updated_items

    items_purchased = item_quantity(items_purchased)
    # calculte the subtotal and total for the bill and tax

    cost = bill(items=items_purchased, tax_rate=tax_rate)

    pos = {"transaction_id": transaction_id,
        "transaction_date": transaction_date}
    pos.update(customer)
    pos['items'] = items_purchased
    pos.update(cost)
    pos['payment_type'] = payment_type['type']
    pos['location'] = store

    print(pos)
    return pos

for i in range(1):
    message = transaction_generator()
    # producer.send(TOPIC, message)
    time.sleep(random.random()*2)

