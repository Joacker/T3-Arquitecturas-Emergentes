import sqlite3

DB_NAME = 'iot_api.db'

# Función para insertar un nuevo administrador
def insert_admin(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Admin (Username, Password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Función para insertar una nueva compañía
def insert_company(company_name, company_api_key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Company (company_name, company_api_key) VALUES (?, ?)', (company_name, company_api_key))
    conn.commit()
    conn.close()

# Función para insertar una nueva ubicación
def insert_location(company_id, location_name, location_country, location_city, location_meta):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Location (company_id, location_name, location_country, location_city, location_meta) VALUES (?, ?, ?, ?, ?)',
                   (company_id, location_name, location_country, location_city, location_meta))
    conn.commit()
    conn.close()

# Función para insertar un nuevo sensor
def insert_sensor(location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Sensor (location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) VALUES (?, ?, ?, ?, ?, ?)',
                   (location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key))
    conn.commit()
    conn.close()

# Función para insertar datos de sensor
def insert_sensor_data(sensor_id, data1, data2):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO SensorData (sensor_id, data1, data2) VALUES (?, ?, ?)', (sensor_id, data1, data2))
    conn.commit()
    conn.close()

# Ejemplo de uso para insertar datos en las tablas
insert_admin('admin', 'admin123')
insert_company('ACME Corp', 'api_key_123')
insert_location(1, 'Oficina Central', 'USA', 'San Francisco', '...')
insert_sensor(1, 1, 'Sensor A', 'Temperatura', '...', 'sensor_api_key_1')
insert_sensor(1, 2, 'Sensor B', 'Humedad', '...', 'sensor_api_key_2')
insert_sensor_data(1, '25', '50')
insert_sensor_data(1, '26', '49')
