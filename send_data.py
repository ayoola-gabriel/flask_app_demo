import requests
import time
import random
from datetime import datetime

url = "http://127.0.0.1:5000/api/logs"


# Simulate sending data every 10 seconds
while True:
    voltage = round(random.uniform(3.0, 4.2), 2)  # Simulate battery voltage
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "name": f"Auto Sensor {timestamp}",
        "battery": voltage
    }

    try:
        response = requests.post(url, json=data)
        print(f"Sent {voltage}V at {timestamp} — Server said: {response.json()['message']}")
    except Exception as e:
        print("❌ Error sending data:", e)

    time.sleep(5)  # Wait for 10 seconds before sending the next data point


