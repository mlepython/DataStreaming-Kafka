import staging

results = staging.query_transaction_id(collection='Customer', field='customer',
                         id='4adf49f0-2e2d-4625-88b4-3b4097c09a35')
print(results)
# TODO coordinate data from staging db to data warehouse
results = staging.get_all_unique_documents(collection='Location', field='location')
for result in results:
    print(result)

# TODO check to see if customer is in data warehous if not update warehouse
# TODO check to see if store location is in data warehouse if not update warehouse
# TODO once a document has been saved to data warehouse, drop from collection
