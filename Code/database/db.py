import sqlite3
from pathlib import Path

# Store the database file inside the database folder
DATABASE_PATH = Path(__file__).resolve().parent / "poultrytrack.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database():
    """Create the sensor readings table if it does not exist."""

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                recorded_at TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()

    print("PoultryTrack database initialised successfully.")


if __name__ == "__main__":
    initialise_database()