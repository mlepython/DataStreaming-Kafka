# TODO the messages from the producer will be consumed here and transformed
# TODO messages will be converted and stored into a data warehouse
# Using the tables for store, inventory, 
from kafka import KafkaConsumer
import json
TOPIC = "PointOfSale"
print('Connecting to Kafka')
# consumer = KafkaConsumer(TOPIC)
consumer = KafkaConsumer(TOPIC, bootstrap_servers='localhost:9092', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
print('Connected to Kafka')
print(f"Reading messages from the topic {TOPIC}")

# Consume messages from the Kafka topic
for message in consumer:
    received_dict = message.value
    print("Received dictionary:", received_dict)

# Close the consumer when done
consumer.close()