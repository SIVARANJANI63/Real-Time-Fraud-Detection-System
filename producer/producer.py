# producer/producer.py

from kafka import KafkaProducer
import json, random, time
from datetime import datetime
from config.config import KAFKA_BROKER, KAFKA_TOPIC

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_transaction():
    return {
        "transaction_id": random.randint(100000, 999999),
        "user_id": random.randint(1, 100),
        "amount": round(random.uniform(10, 1000), 2),
        "location": random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai']),
        "device_info": random.choice(['iOS', 'Android', 'Web']),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    print(f"Producer started. Sending transactions to topic: {KAFKA_TOPIC} at {KAFKA_BROKER}")
    while True:
        txn = generate_transaction()
        try:
            producer.send(KAFKA_TOPIC, value=txn)
            producer.flush()  # ensure message is sent immediately
            print(f"Sent transaction: {txn}")
        except Exception as e:
            print(f"Failed to send transaction: {e}")
        time.sleep(1)
