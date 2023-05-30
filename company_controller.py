from db import get_db


def create_company(company_name, company_api_key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Company (company_name, company_api_key)
        VALUES (?, ?, ?)
    """, (company_name, company_api_key))
    db.commit()
    return {"status": "OK"}

def create_location(company_id, location_name, location_country, location_city, location_meta):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Location (company_id, location_name, location_country, location_city, location_meta)
        VALUES (?, ?, ?, ?, ?)
    """, (company_id, location_name, location_country, location_city, location_meta))
    db.commit()
    return {"status": "OK"}

def create_sensor(location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Sensor (location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key))
    db.commit()
    return {"status": "OK"}
