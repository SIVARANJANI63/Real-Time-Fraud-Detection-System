# dashboard/app.py

from flask import Flask, jsonify
import pandas as pd
import psycopg2
from sklearn.ensemble import IsolationForest
from config.config import POSTGRES

app = Flask(__name__)

@app.route('/anomalies', methods=['GET'])
def anomalies():
    conn = psycopg2.connect(**POSTGRES)
    df = pd.read_sql("SELECT * FROM transactions", conn)
    df_encoded = pd.get_dummies(df[['amount', 'location', 'device_info']])
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(df_encoded)
    df['anomaly'] = model.predict(df_encoded)
    anomalies = df[df['anomaly'] == -1]
    return jsonify(anomalies.to_dict(orient='records'))

if __name__ == "__main__":
    app.run(port=5000, debug=True)
