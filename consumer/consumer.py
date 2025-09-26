# consumer/consumer_db.py

from kafka import KafkaConsumer
import json
import psycopg2
from config.config import KAFKA_BROKER, KAFKA_TOPIC, POSTGRES

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

conn = psycopg2.connect(**POSTGRES)
cursor = conn.cursor()

for message in consumer:
    txn = message.value
    cursor.execute(
        "INSERT INTO transactions (transaction_id, user_id, amount, location, device_info, timestamp) "
        "VALUES (%s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (transaction_id) DO NOTHING",
        (txn['transaction_id'], txn['user_id'], txn['amount'], txn['location'], txn['device_info'], txn['timestamp'])
    )
    conn.commit()
    print(f"Inserted: {txn}")
