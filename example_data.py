import json

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

