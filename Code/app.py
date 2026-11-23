from flask import Flask, render_template, jsonify
from database.db import get_connection
from datetime import datetime, timezone

app = Flask(__name__)


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/readings/latest")
def latest_reading():
    connection = get_connection()

    try:
        reading = connection.execute("""
            SELECT sensor_id, temperature, humidity, recorded_at
            FROM sensor_readings
            ORDER BY id DESC
            LIMIT 1
        """).fetchone()

    finally:
        connection.close()

    if reading is None:
        return jsonify({"message": "No sensor readings available"}), 404

    return jsonify(dict(reading))


from datetime import datetime, timezone


@app.route("/api/sensors/status")
def sensor_status():
    connection = get_connection()

    try:
        reading = connection.execute("""
            SELECT recorded_at
            FROM sensor_readings
            WHERE sensor_id = ?
            ORDER BY id DESC
            LIMIT 1
        """, ("PT-01",)).fetchone()

    finally:
        connection.close()

    if reading is None:
        return jsonify({
            "sensor_id": "PT-01",
            "status": "No readings"
        })

    last_reading = datetime.fromisoformat(
        reading["recorded_at"]
    )

    seconds_since_reading = (
        datetime.now(timezone.utc) - last_reading
    ).total_seconds()

    if 0 <= seconds_since_reading <= 15:
        status = "Reporting"
    else:
        status = "Not reporting"

    return jsonify({
        "sensor_id": "PT-01",
        "status": status,
        "seconds_since_reading": round(
            seconds_since_reading, 1
        )
    })

if __name__ == "__main__":
    app.run(debug=True)
