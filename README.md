# Kafka Consumer and Database Management System

## Overview

This codebase provides a Kafka Consumer designed to receive JSON formatted messages from a Kafka topic, process these messages, and store them into a PostgreSQL database. Additionally, it includes a simulation of point of sale transactions, which can be used to publish messages to a Kafka topic. The companion database scripts handle the creation of database tables, insertion of example data, and the restoration of a database from a backup.

## Dependencies

To run this code successfully, the following prerequisites must be met:

- Kafka: The Kafka Consumer requires a running Apache Kafka environment.
- Python Libraries:
  - `kafka-python`: To interact with Kafka.
  - `SQLAlchemy`: For object-relational mapping (ORM) and database interaction.
  - `psycopg2` or `psycopg2-binary`: PostgreSQL adapter for Python.
  - `python-dotenv`: To manage environment variables.
- PostgreSQL Database: A PostgreSQL server must be running to store the consumed data.
- Environment Variables: PostgreSQL credentials (`PG_USERNAME` and `PG_PASSWORD`) must be set.

## Usage

### Kafka Consumer

Run the consumer script to start consuming messages from a specified Kafka topic. Before running, ensure Kafka is running and available.

```python
consumer = KafkaConsumer(TOPIC, bootstrap_servers='localhost:9092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
```

The above line initiates the Kafka consumer, connecting to the localhost on port 9092.

To run the consumer:

```python
python consumer.py
```

The consumer listens for new messages and processes them by calling update functions with the received JSON data.

### Database Management

Run the `database.py` script to manage the database tables and data. It defines ORM classes for the database structure and provides various update functions to interact with the database.

Ensure environmental variables for PostgreSQL credentials are set, then instantiate the database schema:

```python
Base.metadata.create_all(engine)
```

You can also insert initial values into the tables or run predefined updates with the example data provided.

To run the script in interactive mode:

```python
python -i database.py
```

### Point of Sale Simulator

The `point_of_sale_simulator.py` script simulates point of sale transactions and can send them as messages to a Kafka topic.

```python
message = transaction_generator()  # Generates a mock transaction
# producer.send(TOPIC, message)   # Uncomment to send the message to the Kafka topic
```

To run the simulation:

```python
python point_of_sale_simulator.py
```

### Database Restoration

If you need to restore the database from a backup, use the `restore_database.py` script:

```python
python restore_database.py
```

### Kafka Setup

The `setup_kafka.py` script can be used to download, extract, and start a Kafka instance along with Zookeeper:

```python
python setup_kafka.py
```

## Configuration

To customize the behavior of the code, update the following configurations as necessary:

- Kafka topic name (`TOPIC`)
- Kafka bootstrap servers
- PostgreSQL connection string (`engine = create_engine(...)`)
- Path to `.env` file for environment variables
- Set up initial data by modifying and using the `example_data.py` script

## Key Design Decisions and Patterns

- Use of ORM (SQLAlchemy) to abstract and interact with the database more efficiently.
- Decoupled architecture separating the consumer, database operations, and simulation logic.
- Usage of environment variables for sensitive credential management.

## Improvements

- **Staging database:** Implementing a staging database for the consumer could provide a safer environment for data validation and transformation before updating production databases.
- **Data warehouse:** Transitioning the databases to a data warehouse architecture would help organize the tables into Fact and Dimension categories, enhancing analytics capabilities.
- **ETL:** Establishing ETL (Extract, Transform, Load) processes for regular and automated data movement from transactional systems to the data warehouse.

## Known Limitations and Future Work

- **Kafka security:** Security configurations for Kafka (SSL/TLS, SASL authentication) are not implemented.
- **Database normalization:** The database schema may need further normalization to prevent data redundancy.
- **Error handling:** More robust error handling and logging could be added across different parts of the application.
- **Scaling:** The consumer is not currently set up to scale horizontally. Consumer groups may be needed for larger workloads.

For future improvements, attention should be given to scaling the Kafka consumer, enhancing database performance, and implementing additional features such as monitoring and alerting.