from pymongo import MongoClient
import yaml
from pathlib import Path

# Load staging databse configuration
config_file_path = Path(__file__).parent/'config/staging_config.yaml'
print(config_file_path)
with open(config_file_path, 'r') as config_file:
    config = yaml.safe_load(config_file)


host = config['staging_db']['host']
database = config['staging_db']['database']

# Connect to the MongoDB server
client = MongoClient(f"mongodb://{host}/")
db = client[database]

def update_collection(data: dict):
    collection = db[data['location']['store_id']]
    # print(data)
    # data = data.pop('location')
    
    result = collection.insert_one(data)
    print(f"Inserted document with ID: {result.inserted_id}") 

def transaction_collection(data: dict):
    collection = db['Transactions']
    fields = ['transaction_id', 'transaction_date', 'subtotal',
                       'tax', 'total', 'payment_type']
    new_data = {key: data[key] for key in fields if key in data}
    result = collection.insert_one(new_data)
    print(f"Inserted document with ID: {result.inserted_id}")

def items_collection(data: dict):
    collection = db['Items']
    fields = ['transaction_id', 'transaction_date', 'items']
    new_data = {key: data[key] for key in fields if key in data}
    result = collection.insert_one(new_data)
    print(f"Inserted document with ID: {result.inserted_id}")

def location_collection(data: dict):
    collection = db['Location']
    fields = ['transaction_id', 'transaction_date', 'location']
    new_data = {key: data[key] for key in fields if key in data}
    result = collection.insert_one(new_data)
    print(f"Inserted document with ID: {result.inserted_id}")

def customer_collection(data: dict):
    collection = db['Customer']
    fields = ['transaction_id', 'transaction_date', 'customer']
    new_data = {key: data[key] for key in fields if key in data}
    result = collection.insert_one(new_data)
    print(f"Inserted document with ID: {result.inserted_id}")

def query_transaction_id(collection="", field="", id=""):
    collection = db[collection]
    query = {'transaction_id': id}
    results = collection.find_one(query)
    return results[field]

def get_results(store_id: str):
    collection = db[store_id]
    query = {"city": "New York"}
    results = collection.find(query)
    print(results)

def drop_collection(store_id: str):
    collection = db[store_id]
    collection.drop()
    print(f"Collection dropped: {collection.name}")

def get_customer(store_id: str):
    collection = db[store_id]
    field = "customer"
    distinct_values = collection.distinct(field)
    for customer in distinct_values:
        print("Customer:", customer['customer_id'])
    
    
if __name__=='__main__':
    # drop_collection(store_id='STORE005')
    # get_results(store_id='STORE005')
    # get_customer(store_id='STORE001')
    results = query_transaction_id(collection='Customer', field='customer',
                         id='4adf49f0-2e2d-4625-88b4-3b4097c09a35')
    print(results)