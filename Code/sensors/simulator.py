import random
import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

SENSOR_ID = "PT-01"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = f"poultrytrack/sensors/{SENSOR_ID}/readings"

temperature = 30.0
humidity = 75.0

def generate_reading():
    global temperature, humidity

    temperature += random.uniform(-0.3, 0.3)
    humidity += random.uniform(-1.0, 1.0)

    temperature = round(temperature, 2)
    humidity = round(humidity, 2)

    reading = {
        "sensor_id": SENSOR_ID,
        "temperature": temperature,
        "humidity": humidity,
        "recorded_at": datetime.now(timezone.utc).isoformat()
    }

    return reading



if __name__ == "__main__":
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2
    )

    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()

        print("PoultryTrack MQTT sensor simulator started.")

        while True:
            reading = generate_reading()

            message = json.dumps(reading)

            result = client.publish(
                MQTT_TOPIC,
                message,
                qos=1
            )

            result.wait_for_publish()

            print(f"Published: {message}")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nSensor simulator stopped.")

    except OSError as error:
        print(f"MQTT connection error: {error}")

    finally:
        client.disconnect()
        client.loop_stop()
