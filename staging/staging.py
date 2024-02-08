from pymongo import MongoClient
import yaml
from pathlib import Path

# Load staging databse configuration
config_file_path = Path(__file__).parent.parent/'config/staging_config.yaml'
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
    result = collection.insert_one(data.pop('location'))
    print(f"Inserted document with ID: {result.inserted_id}") 

def get_collection(store_id: str):
    collection = db[store_id]
    
# # Access a collection within the database
# collection = db["mycollection"]
# collection = db['new_collection']

# # Insert a document into the collection
# document = {"name": "John Doe", "age": 30, "city": "New York"}
# result = collection.insert_one(document)

# print(f"Inserted document with ID: {result.inserted_id}")
# # Find documents in the collection
# query = {"city": "New York"}
# results = collection.find(query)

# for result in results:
#     print(result)
