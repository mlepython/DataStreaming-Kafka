# Point Of Sale System

The code provided consists of several Python scripts aimed at simulating a point of sale system. Below is a breakdown of each file's purpose and functionality.

## Files Overview

1. `consumer.py`: Defines a Kafka consumer that reads messages from the "PointOfSale" topic and updates corresponding database tables with the received data.
2. `database.py`: Contains SQLAlchemy models for database tables related to transactions, items purchased, inventory, dates, stores, payment options, tax rates, and customers. It also includes functions to update these tables based on incoming data. 
3. `example_data.py`: Provides example data in JSON format for groceries, inventory, payment options, store locations, Canadian tax rates, Canadian customers, and sample point of sale transactions.
4. `point_of_sale_simulator.py`: Generates random transactions with various data elements and sends them to a Kafka topic for processing.
5. `restore_database.py`: Restores a PostgreSQL database schema using a SQL dump file.
6. `setup_kafka.py`: Downloads and sets up a Kafka instance for message queuing.

## Dependencies

To run the code snippets successfully, the following dependencies are needed:
- Kafka (for `consumer.py` and `point_of_sale_simulator.py`)
- SQLAlchemy
- psycopg2
- dotenv
- Python 3.x

## How to Run

1. Ensure that Kafka is set up and running.
2. Run `restore_database.py` to restore the PostgreSQL database schema.
3. Update the database connection details in `database.py` if necessary.
4. Execute `point_of_sale_simulator.py` to generate random transactions and send them to the Kafka topic "PointOfSale".
5. Run `consumer.py` to consume messages from the Kafka topic, updating the database tables with the received data.

## Design Decisions

- Data is processed using SQLAlchemy ORM models to organize and store transaction-related information.
- Faker functions are used to generate random data elements for transactions.
- Kafka messaging system is employed for communication between the producer and consumer scripts.

## Future Improvements

- Add error handling and logging mechanisms for better debugging.
- Implement additional data validation and integrity checks for database updates.
- Create unit tests to ensure the correctness of database operations under various scenarios.

In conclusion, this set of scripts provides a basic framework for simulating transactions in a point of sale system, utilizing Kafka as the messaging backbone and a PostgreSQL database to store transaction data. Feel free to explore and enhance the functionality based on your specific requirements.
