import staging
import data_warehouse

# get all transactions stored in mongo
transactions = staging.get_all_transactions()
for transaction in transactions:
    print(transaction)
    # for each transaction, insert values into data warehouse
    id=transaction['transaction_id']
    customer = staging.query_transaction_id(collection='Customer', field='customer', id=id)
    location = staging.query_transaction_id(collection='Location', field='location', id=id)
    items = staging.query_transaction_id(collection='Items', field='items', id=id)
    print(items)

    # results = staging.get_all_unique_documents(collection='Location', field='location')
    # for result in results:
    #     print(result)

    data_warehouse.update_transaction_table(data=transaction,
                                            customer_id=customer['customer_id'],
                                            store_id=location['store_id'])
    data_warehouse.updated_items_purchased_table(data=items, transaction_id=id)
    # check to see if customer is in data warehous if not update warehouse
    data_warehouse.update_customer_table(data=customer)
    # check to see if store location is in data warehouse if not update warehouse
    data_warehouse.update_store_table(data=location)
    # add date to date table
    data_warehouse.update_date_table(data=transaction)
    # TODO once a document has been saved to data warehouse, drop from collection
