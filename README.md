# Kafka Consumer for Point of Sale System

## Overview
This codebase comprises a set of Python scripts designed to ingest transactional data from a Kafka topic named "PointOfSale", process and store it in different databases, stage the data for transformation, and finally, integrate into a data warehouse. It includes a Kafka consumer, database operations, data staging, and a transaction producer for simulating point of sale data.

## Dependencies
- Python 3.x
- Kafka (including Zookeeper)
- MongoDB
- PostgreSQL
- SQLAlchemy
- Python-dotenv
- PyMongo
- Kafka-Python library

## Usage

### Kafka Consumer (`consumer.py`)
The Kafka consumer script is responsible for consuming messages from the Kafka "PointOfSale" topic, processing the received data and inserting it into a staging area, and then updating several collections, potentially for further ETL processes.

To run the consumer script, use the following command:

```bash
python consumer.py
```

### Database Operations (`database.py`)
This script defines the database schema using SQLAlchemy ORM and provides functions to interact with the PostgreSQL database. It includes transactional tables, inventory, and customer data models.

In addition to creating the schema, it also provides functions to update the transaction, items purchased, and date tables. Before running this script, ensure you have set the correct environment variables for the PostgreSQL database credentials.

### Data Staging (`staging.py`)
The staging script contains functions to interact with the MongoDB collections, which store transactional data temporarily before it's processed into the data warehouse. It connects to MongoDB, inserts documents, and retrieves data by transactions for further processing.

### Main Processing (`main.py`)
The main script coordinates the process of transforming and loading data from the staging area into the actual data warehouse.

### Transaction Producer (`producer.py`)
This script simulates a stream of transaction data and sends it to the Kafka "PointOfSale" topic. It generates random transaction entries and serializes them into JSON format before sending them through Kafka.

To simulate transaction data, run the following command:

```bash
python producer.py
```

### Store Inventory Database (`store_inventory_db.py`)
This script sets up a PostgreSQL database to manage the inventory for multiple stores. It creates an inventory table and inserts items for each store.

### Setup Kafka (`setup_kafka.py`)
Contains instructions for downloading and setting up Apache Kafka and Zookeeper on your local machine.

## Configuration
The codebase includes configurations for Kafka, MongoDB, and PostgreSQL databases. Before running any scripts, you must set up the `.env` file with the correct database credentials for PostgreSQL, and `staging_config.yaml` for MongoDB connection details.

## Design Decisions
- Kafka for real-time data streaming.
- SQLAlchemy ORM for database interaction abstraction.
- MongoDB for staging the data allows for flexible schema and easy integration with other systems.
- PostgreSQL for structured and relational data storage.

## Future Improvements and How to Implement Them
- Implement a staging database that temporarily holds data for processing: Introduce an intermediate relational database dedicated to staging data before it is transformed and stored in the data warehouse.
- Set up a data warehouse: Design a schema with Fact and Dimension tables to support OLAP operations and better analytics. Creating a Star or Snowflake schema can allow for more complex queries and reports.
- Develop ETL (Extract, Transform, Load) processes: Create a series of scripts or use an ETL framework to automate the transformation and loading of data from the staging database into the data warehouse. This might include data cleaning, normalization, and denormalization steps.
- Use a workflow management tool such as Apache Airflow to orchestrate the ETL pipelines, ensuring that data is accurately transferred at scheduled intervals and dependencies are managed effectively.