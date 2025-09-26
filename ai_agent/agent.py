# ai_agent/ai_agent.py

import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest
from config.config import POSTGRES

conn = psycopg2.connect(**POSTGRES)
df = pd.read_sql("SELECT * FROM transactions", conn)

# One-hot encode categorical columns
df_encoded = pd.get_dummies(df[['amount', 'location', 'device_info']])

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(df_encoded)

df['anomaly'] = model.predict(df_encoded)
df['risk_score'] = model.decision_function(df_encoded)

anomalies = df[df['anomaly'] == -1]
print("Anomalous transactions:\n", anomalies[['transaction_id', 'amount', 'risk_score']])
