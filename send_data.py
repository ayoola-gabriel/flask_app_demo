import requests
import time
import random
from datetime import datetime

# url = "https://flask-app-demo-mgz7.onrender.com/api/logs"
url = "http://127.0.0.1:5000/api/logs"  # Change to your local or remote URL

headers = {
    "Content-Type": "application/json",
    "x-api-key": "newnss-secret-key-with-flask-2025"  # 👈 Must match app.py
}

# Simulate sending data every 10 seconds
while True:
    voltage = round(random.uniform(3.0, 4.2), 2)  # Simulate battery voltage
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "name": f"{timestamp}",
        "battery": voltage
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"Sent {voltage}V at {timestamp} — Server said: {response.json()['message']}")
    except Exception as e:
        print("❌ Error sending data:", e)

    time.sleep(5)  # Wait for 10 seconds before sending the next data point


