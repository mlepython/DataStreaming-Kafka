# Kafka Point-of-Sale Data Processing README

## Overview

This codebase is designed to simulate a Point-of-Sale (POS) system, specifically focusing on the generation, consumption, and storage of sales transaction data. The provided Python scripts work together to:

- Simulate POS transactions (`point_of_sale_simulator.py`)
- Send generated transactions to a Kafka topic
- Consume messages from a Kafka topic (`consumer.py`)
- Update a PostgreSQL database with the received transaction data (`database.py`)

## Dependencies

- Python 3.x
- Kafka (installation and CLI tools)
- SQLAlachemy for ORM
- PostgreSQL database
- python-dotenv for environment variable management
- Additional Python libraries: json, datetime, os, uuid

## Installation

Ensure Python 3.x and PostgreSQL are installed on your system.

Install required Python packages using:
```bash
pip install kafka-python sqlalchemy psycopg2 python-dotenv
```

For Kafka setup and usage follow the official documentation at: https://kafka.apache.org/documentation/

Set up environment variables for your PostgreSQL connection in a `.env` file with the following entries:
```
PG_USERNAME=your_username
PG_PASSWORD=your_password
```

## Using the Code

### Producer Script: Point-of-Sale Simulator

The `point_of_sale_simulator.py` file simulates POS transaction events. Run the script to generate and send transaction data to a Kafka topic. Ensure Kafka server and Zookeeper are running.

### Consumer Script

The `consumer.py` file acts as a Kafka consumer which listens to a specified Kafka topic. Upon receiving messages, it processes the data and updates the respective database tables. Ensure you have modified the database credentials and have the correct Kafka topic and broker specified.

### Database Script

The `database.py` file contains all the SQLAlchemy ORM classes for the database tables, database connection setup, and functions to update each table. It also contains the execution code to populate the database with initial data from `example_data.py`.

### Initial Data and Restoration

The `example_data.py` script provides example data for simulation purposes. To restore the database to a previous state, use the `restore_database.py` script.

## Code Examples

### Consuming Messages

To consume messages from the Kafka queue, ensure the Kafka server is up and running. Then, execute the `consumer.py` script:

```python
# Start consuming messages from Kafka topic
for message in consumer:
    received_dict = message.value
    update_transaction_table(data=received_dict)
    updated_items_purchased_table(data=received_dict)
    update_date_table(data=received_dict)
```

### Updating Database Tables

To update the `transactions` table with new data:

```python
def update_transaction_table(data):
    # Function body here...
    session.commit()
```

## Configuration

Make sure the Kafka bootstrap server address and topic name in both the producer and the consumer match. Modify `TOPIC` and `bootstrap_servers` as needed.

## Design Decisions and Patterns

- Used ORM (SQLAlchemy) for database interactions to simplify code and improve maintainability.
- Used Kafka for message queuing and processing to allow for real-time data streaming and scalable architecture.
- Adopted the Environmental Variables pattern for managing sensitive configuration such as database credentials.

## Known Issues and Limitations

The current database structure operates as an operational database. There is no separation between staging, operational, and analytical databases.

## Future Improvements

- **Staging Database**: Implement a staging area to hold raw data from Kafka before cleaning and transforming it for operational or analytical purposes. This can be achieved by creating a separate schema or database that temporarily stores incoming data.
- **Data Warehouse**: Transition the current database to serve as an OLTP (Online Transaction Processing) system and create a separate OLAP (Online Analytical Processing) data warehouse. Tables can be structured into fact and dimension tables to support complex analytical queries.
- **ETL Process**: Establish an ETL (Extract, Transform, Load) pipeline to move data from the staging area to both the operational database and the data warehouse, ensuring data is properly transformed and suitable for both transactional operations and analytics.

To implement these changes, additional scripts and database schemas would have to be developed, requiring a solid understanding of business logic and data modeling best practices. Tools like Apache Airflow for scheduling ETL jobs, or services such as AWS Glue, could be considered to manage the ETL workflows effectively.