import sqlite3

DB_NAME = 'iot_api.db'

# Crear la tabla Admin
def create_admin_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Admin (
            Username TEXT,
            Password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Crear la tabla Company
def create_company_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Company (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            company_api_key TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Crear la tabla Location
def create_location_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Location (
            company_id INTEGER,
            location_name TEXT,
            location_country TEXT,
            location_city TEXT,
            location_meta TEXT,
            FOREIGN KEY (company_id) REFERENCES Company (ID)
        )
    ''')
    conn.commit()
    conn.close()

# Crear la tabla Sensor
def create_sensor_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sensor (
            location_id INTEGER,
            sensor_id INTEGER,
            sensor_name TEXT,
            sensor_category TEXT,
            sensor_meta TEXT,
            sensor_api_key TEXT,
            FOREIGN KEY (location_id) REFERENCES Location (ID)
        )
    ''')
    conn.commit()
    conn.close()

# Crear la tabla SensorData
def create_sensor_data_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS SensorData (
            sensor_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            data1 TEXT,
            data2 TEXT,
            FOREIGN KEY (sensor_id) REFERENCES Sensor (ID)
        )
    ''')
    conn.commit()
    conn.close()

# Función para crear todas las tablas
def create_tables():
    create_admin_table()
    create_company_table()
    create_location_table()
    create_sensor_table()
    create_sensor_data_table()

# Llamada a la función para crear las tablas
create_tables()

