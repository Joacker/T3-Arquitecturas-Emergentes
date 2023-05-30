import sqlite3

DATABASE_NAME = "flask-api.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    tables = [
        """
        CREATE TABLE Admin (
           Username TEXT,
           Password TEXT
        );
        """,
        """
        CREATE TABLE Company (
           ID INTEGER,
           company_name TEXT,
           company_api_key TEXT,
           PRIMARY KEY (ID)
        );
        """,
        """
        CREATE TABLE Location (
           company_id INTEGER,
           location_name TEXT,
           location_country TEXT,
           location_city TEXT,
           location_meta TEXT,
           FOREIGN KEY (company_id) REFERENCES Company(ID)
        );
        """,
        """
        CREATE TABLE Sensor (
           location_id INTEGER,
           sensor_id INTEGER,
           sensor_name TEXT,
           sensor_category TEXT,
           sensor_meta TEXT,
           sensor_api_key TEXT,
           FOREIGN KEY (location_id) REFERENCES Location(rowid)
        );
        """,
        """
        CREATE TABLE SensorData (
           sensor_id INTEGER,
           timestamp DATETIME,
           value REAL,
           -- Add more columns based on specific sensor data
           FOREIGN KEY (sensor_id) REFERENCES Sensor(rowid)
        );
        """
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)

# Call the create_tables function to create the tables
create_tables()
