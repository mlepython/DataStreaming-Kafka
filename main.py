import staging
import data_warehouse
import time


def transfer_from_mongo_to_warehouse():
    # get all transactions stored in mongo 'Transactions' collection
    transactions = staging.get_all_transactions()
    for transaction in transactions:
        # for each transaction, insert values into data warehouse
        id=transaction['transaction_id']
        print(f"Transaction id: {id}")
        customer = staging.query_transaction_id(collection='Customer', field='customer', id=id)
        location = staging.query_transaction_id(collection='Location', field='location', id=id)
        items = staging.query_transaction_id(collection='Items', field='items', id=id)

        # results = staging.get_all_unique_documents(collection='Location', field='location')
        # for result in results:
        #     print(result)
        if customer and location and items:
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
            # once a document has been saved to data warehouse, drop from collection
            staging.drop_document(collection='Customer', id=id)
            staging.drop_document(collection='Location', id=id)
            staging.drop_document(collection='Items', id=id)
            staging.drop_document(collection='Transactions', id=id)

timeout = 0
while timeout <= 60:
    total_documents = staging.total_documents()
    if total_documents > 100:
        transfer_from_mongo_to_warehouse()
        timeout = 0
    else:
        print(f'Waiting for new documents: timeout {timeout}')
    timeout += 1
    time.sleep(1)

if total_documents > 0:
    transfer_from_mongo_to_warehouse()