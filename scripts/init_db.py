# scripts/init_db.py

import psycopg2
from config.config import POSTGRES

conn = psycopg2.connect(**POSTGRES)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id BIGINT PRIMARY KEY,
    user_id INT,
    amount FLOAT,
    location VARCHAR(50),
    device_info VARCHAR(50),
    timestamp TIMESTAMP
)
""")
conn.commit()
print("Database initialized.")
