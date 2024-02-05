# Point Of Sale Data Processing System

## Overview

This system consists of several components working together to simulate, process, and store point of sale transactions, as might be seen in a retail environment. It involves a Kafka producer simulating transactions (`point_of_sale_simulator.py`), a Kafka consumer processing those transactions (`consumer.py`), and a database schema and interface (`database.py`) for storing the transaction data persistently. Additionally, it includes support scripts to set up Kafka (`setup_kafka.py`) and to restore a database (`restore_database.py`), as well as helper code that provides sample data (`example_data.py`).

Key functionalities include:

- Simulating point of sale transactions with varying items, quantities, customers, and locations.
- Consuming messages from a Kafka topic and updating a database accordingly.
- Mapping and persisting data to PostgreSQL, including handling payment options, tax rates, and customer information.
- Easy-to-use environment setup via provided setup scripts for both Kafka and the PostgreSQL database.

## Dependencies

To run this code successfully, ensure the following dependencies are installed:

- Python 3.x
- kafka-python (`pip install kafka-python`)
- SQLAlchemy (`pip install SQLAlchemy`)
- psycopg2 or psycopg2-binary (`pip install psycopg2-binary`)
- python-dotenv (`pip install python-dotenv`)
- Ensure Kafka and Zookeeper are installed and properly configured.

## Usage

### Setting Up the Environment

First, you must have a Kafka and Zookeeper instance running. To help in setting up Kafka, you can use the included `setup_kafka.py` script, which downloads and extracts Kafka, then starts both the Kafka server and Zookeeper.

For the database, a PostgreSQL instance must be set up, and the schema should be created as defined in `database.py`. You can use the `restore_database.py` script to restore the database from a backup if needed.

Ensure that you have a `.env` file with PostgreSQL credentials set up:

```
PG_USERNAME=your_username
PG_PASSWORD=your_password
```

### Starting the Consumer

To start consuming messages from the Kafka topic, run the consumer script:

```python
python consumer.py
```

This script will listen to the Kafka topic `PointOfSale` and process incoming messages by updating the transaction, items purchased, and date tables in the PostgreSQL database.

### Running the POS Simulator

The point of sale (POS) simulator can be used to generate and send messages to the configured Kafka topic. 

```python
python point_of_sale_simulator.py
```

This will generate transaction data, simulate customer behavior, and push these transactions to Kafka, where they can be consumed by the consumer script.

### Interacting with the Database

The `database.py` contains the ORM definitions for the database tables and several functions to update those tables. You can interact with the database using these functions or extend the functionality as per your requirements.

## Design Decisions and Patterns

- The project's codebase uses the **ORM (Object-Relational Mapping)** pattern via SQLAlchemy to abstract database interactions, making it more maintainable and portable.
- A **decoupled architecture** is used where the producer and consumer operate independently, which allows for scalability and fault tolerance.
- **Environment variable** usage for database credentials promotes security and flexibility for different deployment environments.

## Known Issues and Future Improvements

- The `database.py` file contains `TODO` comments mentioning that a database connection needs to be established and dimension tables for product, location, customer, and date need to be implemented.
- The transaction generator currently has a fixed set of possible customers and items that can be randomly selected. Real-world scenarios would involve a dynamic and potentially much larger set of options.
- The Kafka Producer instance creation is currently commented out; it should be activated and configured correctly to produce messages to the Kafka topic.
- Error handling and retry mechanisms may need to be improved for more robust production use.

## Code Examples

Example for updating transaction table after consuming a Kafka message:

```python
# Assuming `received_dict` is the dictionary received from the Kafka topic `PointOfSale`
update_transaction_table(data=received_dict)
```

Starting the Kafka consumer and waiting for messages on the topic `PointOfSale`:

```python
consumer = KafkaConsumer(TOPIC, bootstrap_servers='localhost:9092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
for message in consumer:
    process_message(message.value)
```

Persistently updating the database with SQLAlchemy:

```python
session.add(NewRow(...))
session.commit()
```

## Conclusion

The Point of Sale Data Processing System provided in these scripts demonstrates the integration of a Kafka message broker with a database backend, simulating a realistic data flow scenario in retail transactions. The code is modular and designed for easy expansion and customization to suit varied end-use cases in transaction processing.