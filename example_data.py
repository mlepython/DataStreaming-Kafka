import json
from random import randint

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

items = read_json('./data/groceries.json')
items = items['grocery_list']

inventory = read_json('./data/inventory.json')
inventory = inventory['inventory']

payment_options = read_json('./data/payment_options.json')
payment_options = payment_options['payment_options']

store_locations = read_json('./data/store_locations.json')
store_locations = store_locations['store_locations']

canadian_tax_rates = read_json('./data/canadian_tax_rates.json')
canadian_tax_rates = canadian_tax_rates['canadian_tax_rates']

canadian_customers = read_json('./data/canadian_customers.json')
canadian_customers = canadian_customers['canadian_customers']

pos_example = read_json('./data/pos_example.json')
pos_example_2 = read_json('./data/pos_example_2.json')
pos_example_3 = read_json('./data/pos_example_3.json')

