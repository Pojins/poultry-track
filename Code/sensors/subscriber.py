
import json
import sqlite3
from pathlib import Path

import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "poultrytrack/sensors/+/readings"

DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "database"
    / "poultrytrack.db"
)


def validate_reading(reading):
    required_fields = [
        "sensor_id",
        "temperature",
        "humidity",
        "recorded_at"
    ]

    for field in required_fields:
        if field not in reading:
            return False

    if not isinstance(reading["sensor_id"], str):
        return False

    if not reading["sensor_id"].strip():
        return False

    if type(reading["temperature"]) not in (int, float):
        return False

    if type(reading["humidity"]) not in (int, float):
        return False

    if not -10 <= reading["temperature"] <= 60:
        return False

    if not 0 <= reading["humidity"] <= 100:
        return False

    return True

def save_reading(reading):
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("""
            INSERT INTO sensor_readings
                (sensor_id, temperature, humidity, recorded_at)
            VALUES (?, ?, ?, ?)
        """, (
            reading["sensor_id"],
            reading["temperature"],
            reading["humidity"],
            reading["recorded_at"]
        ))

        connection.commit()

    finally:
        connection.close()


def on_message(client, userdata, message):
    print("New MQTT message received!")

    try:
        payload = message.payload.decode("utf-8")
        reading = json.loads(payload)

        if not isinstance(reading, dict):
            print("Invalid message: expected a JSON object.")
            return

        if not validate_reading(reading):
            print("Invalid sensor reading. Message rejected.")
            return

        print(f"Valid reading from {reading['sensor_id']}")
        print(f"Temperature: {reading['temperature']} °C")
        print(f"Humidity: {reading['humidity']} %")
        print(f"Recorded at: {reading['recorded_at']}")

        try:
            save_reading(reading)
            print("Reading saved to SQLite successfully.")

        except sqlite3.Error as error:
            print(f"Database error: {error}")

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Could not decode message: {error}")


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker.")
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"Subscribed to: {MQTT_TOPIC}")
    else:
        print(f"MQTT connection failed: {reason_code}")


if __name__ == "__main__":
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("Waiting for sensor readings...")
        client.loop_forever()

    except KeyboardInterrupt:
        print("\nSubscriber stopped.")

    except OSError as error:
        print(f"MQTT connection error: {error}")

    finally:
        client.disconnect()
