import json
import paho.mqtt.publish as publish

reading = {
    "sensor_id": "PT-01",
    "temperature": 30,
    "humidity": 150,
    "recorded_at": "2026-11-17T20:30:00+00:00"
}

message = json.dumps(reading)

publish.single(
    "poultrytrack/sensors/PT-01/readings",
    message,
    hostname="localhost"
)

print("Invalid test reading published.")
