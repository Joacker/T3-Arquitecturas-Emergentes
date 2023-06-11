from crypt import methods
import sqlite3
from app import app
from flask import jsonify, request,abort,make_response
from datetime import datetime
import jwt
from functools import wraps
from Connect import connection
import json
from __init__db__ import create_tables

# from auth import token_required,api_company_req,api_sensor_req
# import Locations
# import Sensors
# import Sensors_data

#API's

@app.route('/',methods=['GET'])
def index():
    return jsonify({"message":"Welcome to the API"})

#GET ADMINS
@app.route('/admin',methods=['GET'])
def get_admin():
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Admin")
    rows = c.fetchall()
    con.close()
    Admins = []
    for i in rows:
        get_Admin = {}
        get_Admin["USERNAME"] = i["USERNAME"]
        get_Admin["PASSWORD"] = i["PASSWORD"]
        Admins.append(get_Admin)
    return jsonify(Admins)

#REGISTER ADMIN
@app.route('/admin',methods=['POST'])
def register_admin():
    con = connection()
    c = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    
    if not username:
        return jsonify({"message":"Username is required"}),400
    
    if not password:
        return jsonify({"message":"Password is required"}),400
    
    # validate if exist the admin
    if c.execute("SELECT * FROM Admin WHERE Username = ?",(username,)).fetchone() is not None:
        return jsonify({"message":"Admin already exist"}),400
    

    c.execute("INSERT INTO Admin (Username,Password) VALUES (?,?)",(username,password))
    con.commit()
    con.close()
    return jsonify({"message":"Admin created"})

# Create Company
@app.route('/create_company',methods=['POST'])
def create_company():
    con = connection()
    c = con.cursor()
    data = request.get_json()
    company_name = data['company_name']
    company_api_key = data['company_api_key']
    if c.execute("SELECT * FROM Company WHERE Company_Name = ?",(company_name,)).fetchone() is not None:
        return jsonify({"message":"Company already exist"}),400
    c.execute("INSERT INTO Company (Company_Name,Company_API_Key) VALUES (?,?)",(company_name,company_api_key))
    con.commit()
    con.close()
    return jsonify({"message":"Company created"})

# Get Company
@app.route('/get_company',methods=['GET'])
def get_company():
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Company")
    rows = c.fetchall()
    con.close()
    Company = [{"ID": i["ID"], "Company_Name": i["Company_Name"], "Company_API_Key": i["Company_API_Key"]} for i in rows]
    return jsonify(Company)


# GET LOCATIONS
@app.route('/locations',methods=['GET'])
def get_locations():
    try:
        with connection() as con:
            c = con.cursor()          
            c.execute("SELECT * FROM Location")
            rows = c.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    Locations = []
    for i in rows:
        get_Location = {}
        get_Location["ID"] = i["ID"]
        get_Location["company_id"] = i["company_id"]
        get_Location["location_name"] = i["location_name"]
        get_Location["location_country"] = i["location_country"]
        get_Location["location_city"] = i["location_city"]
        get_Location["location_meta"] = i["location_meta"]
        Locations.append(get_Location)
    return jsonify(Locations)


# GET LOCATION BY ID
@app.route('/locations/<int:id>',methods=['GET'])
def get_location(id):
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Location WHERE ID = ?",(id,))
    row = c.fetchone()
    con.close()
    
    # Validate if the location exist
    if row is None:
        return jsonify({"message":"Location does not exist"}),400
    
    get_Location = {}
    get_Location["company_id"] = row["company_id"]
    get_Location["location_name"] = row["location_name"]
    get_Location["location_country"] = row["location_country"]
    get_Location["location_city"] = row["location_city"]
    get_Location["location_meta"] = row["location_meta"]
    return jsonify(get_Location)


# REGISTER LOCATION
@app.route('/locations',methods=['POST'])
def register_location():
    con = connection()
    c = con.cursor()
    data = request.get_json()
    companyid = data['company_id']
    name = data['location_name']
    country = data['location_country']
    city = data['location_city']
    meta = data['location_meta']

    if not companyid:
        return jsonify({"message":"Company ID is required"}),400
    
    if not name:
        return jsonify({"message":"Name is required"}),400
    
    if not country:
        return jsonify({"message":"Country is required"}),400
    
    if not city:
        return jsonify({"message":"City is required"}),400
    
    if not meta:
        return jsonify({"message":"Meta is required"}),400

    # validate if exist the company does not exist
    if c.execute("SELECT * FROM Company WHERE ID = ?",(companyid,)).fetchone() is None:
        return jsonify({"message":"Company does not exist"}),400

    # validate if exist the location
    if c.execute("SELECT * FROM Location WHERE location_name = ?",(name,)).fetchone() is not None:
        return jsonify({"message":"Location already exist"}),400
    
    c.execute("INSERT INTO Location (company_id,location_name,location_country,location_city,location_meta) VALUES (?,?,?,?,?)",(companyid,name,country,city,meta))
    con.commit()
    con.close()
    return jsonify({"message":"Location created"})



# UPDATE LOCATION
@app.route('/locations/<int:id>',methods=['PUT'])
def update_location(id):
    con = connection()
    c = con.cursor()
    data = request.get_json()
    companyid = data['company_id']
    name = data['location_name']
    country = data['location_country']
    city = data['location_city']
    meta = data['location_meta']

    if not companyid:
        return jsonify({"message":"Company ID is required"}),400
    
    if not name:
        return jsonify({"message":"Name is required"}),400
    
    if not country:
        return jsonify({"message":"Country is required"}),400
    
    if not city:
        return jsonify({"message":"City is required"}),400
    
    if not meta:
        return jsonify({"message":"Meta is required"}),400
    
    # validate if exist the company does not exist
    if c.execute("SELECT * FROM Company WHERE ID = ?",(companyid,)).fetchone() is None:
        return jsonify({"message":"Company does not exist"}),400
    
    # validate if exist the location
    if c.execute("SELECT * FROM Location WHERE ID = ?",(id,)).fetchone() is None:
        return jsonify({"message":"Location does not exist"}),400
    
    c.execute("UPDATE Location SET company_id = ?, location_name = ?, location_country = ?, location_city = ?, location_meta = ? WHERE ID = ?",(companyid,name,country,city,meta,id))
    con.commit()
    con.close()
    return jsonify({"message":"Location updated"})


# DELETE LOCATION
@app.route('/locations/<int:id>',methods=['DELETE'])
def delete_location(id):
    con = connection()
    c = con.cursor()

    # validate if exist the location
    if c.execute("SELECT * FROM Location WHERE ID = ?",(id,)).fetchone() is None:
        return jsonify({"message":"Location does not exist"}),400
    
    c.execute("DELETE FROM Location WHERE ID = ?",(id,))
    con.commit()
    con.close()
    return jsonify({"message":"Location deleted"})

# GET SENSORS
@app.route('/sensors',methods=['GET'])
def get_sensors():
    try:
        with connection() as con:
            c = con.cursor()
            c.execute("SELECT * FROM Sensor")
            rows = c.fetchall()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    Sensors = []
    for i in rows:
        get_Sensor = {}
        get_Sensor["ID"] = i["ID"]
        get_Sensor["location_id"] = i["location_id"]
        get_Sensor["sensor_name"] = i["sensor_name"]
        get_Sensor["sensor_category"] = i["sensor_category"]
        get_Sensor["sensor_meta"] = i["sensor_meta"]
        get_Sensor["sensor_api_key"] = i["sensor_api_key"]
        Sensors.append(get_Sensor)
    return jsonify(Sensors)

# GET SENSOR BY ID
@app.route('/sensors/<int:id>',methods=['GET'])
def get_sensor(id):
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Sensor WHERE ID = ?",(id,))
    row = c.fetchone()
    con.close()
    if row is None:
        return jsonify({"message":"Sensor does not exist"}),400
    get_Sensor = {}
    get_Sensor["location_id"] = row["location_id"]
    get_Sensor["sensor_name"] = row["sensor_name"]
    get_Sensor["sensor_category"] = row["sensor_category"]
    get_Sensor["sensor_meta"] = row["sensor_meta"]
    get_Sensor["sensor_api_key"] = row["sensor_api_key"]
    return jsonify(get_Sensor)

# REGISTER SENSOR
@app.route('/sensors',methods=['POST'])
def register_sensor():
    con = connection()
    c = con.cursor()
    data = request.get_json()
    locationid = data['location_id']
    name = data['sensor_name']
    category = data['sensor_category']
    meta = data['sensor_meta']
    apikey = data['sensor_api_key']

    if not locationid:
        return jsonify({"message":"Location ID is required"}),400
    
    if not name:
        return jsonify({"message":"Name is required"}),400
    
    if not category:
        return jsonify({"message":"Category is required"}),400
    
    if not meta:
        return jsonify({"message":"Meta is required"}),400
    
    if not apikey:
        return jsonify({"message":"API Key is required"}),400

    # validate if exist the location does not exist
    if c.execute("SELECT * FROM Location WHERE ID = ?",(locationid,)).fetchone() is None:
        return jsonify({"message":"Location does not exist"}),400

    # validate if exist the sensor
    if c.execute("SELECT * FROM Sensor WHERE sensor_name = ?",(name,)).fetchone() is not None:
        return jsonify({"message":"Sensor already exist"}),400
    
    c.execute("INSERT INTO Sensor (location_id,sensor_name,sensor_category,sensor_meta,sensor_api_key) VALUES (?,?,?,?,?)",(locationid,name,category,meta,apikey))
    con.commit()
    con.close()
    return jsonify({"message":"Sensor created"})

# UPDATE SENSOR
@app.route('/sensors/<int:id>',methods=['PUT'])
def update_sensor(id):
    con = connection()
    c = con.cursor()
    data = request.get_json()
    locationid = data['location_id']
    name = data['sensor_name']
    category = data['sensor_category']
    meta = data['sensor_meta']
    apikey = data['sensor_api_key']

    if not locationid:
        return jsonify({"message":"Location ID is required"}),400
    
    if not name:
        return jsonify({"message":"Name is required"}),400
    
    if not category:
        return jsonify({"message":"Category is required"}),400
    
    if not meta:
        return jsonify({"message":"Meta is required"}),400
    
    if not apikey:
        return jsonify({"message":"API Key is required"}),400

    # validate if exist the location does not exist
    if c.execute("SELECT * FROM Location WHERE ID = ?",(locationid,)).fetchone() is None:
        return jsonify({"message":"Location does not exist"}),400

    # validate if exist the sensor
    if c.execute("SELECT * FROM Sensor WHERE ID = ?",(id,)).fetchone() is None:
        return jsonify({"message":"Sensor does not exist"}),400
    
    c.execute("UPDATE Sensor SET location_id = ?, sensor_name = ?, sensor_category = ?, sensor_meta = ?, sensor_api_key = ? WHERE ID = ?",(locationid,name,category,meta,apikey,id))
    con.commit()
    con.close()
    return jsonify({"message":"Sensor updated"})

# DELETE SENSOR
@app.route('/sensors/<int:id>',methods=['DELETE'])
def delete_sensor(id):
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Sensor WHERE ID = ?",(id,))
    row = c.fetchone()
    if row is None:
        return jsonify({"message":"Sensor not found"}),404
    c.execute("DELETE FROM Sensor WHERE ID = ?",(id,))
    con.commit()
    con.close()
    return jsonify({"message":"Sensor deleted"})

# REGISTER SENSOR DATA
@app.route('/sensor_data',methods=['POST'])
def register_sensor_data(sensor_api_key):
    con = connection()
    c = con.cursor()
    data = request.get_json()
    sensor_id = data['sensor_id']
    time = data['data']['time']
    temperature = data['data']['temperature']
    humidity = data['data']['humidity']
    distance = data['data']['distance']
    pressure = data['data']['pressure']
    light_level = data['data']['light_level']

    if not sensor_id:
        return jsonify({"message":"Sensor ID is required"}),400
    
    if not time:
        return jsonify({"message":"Time is required"}),400
    
    if not temperature:
        return jsonify({"message":"Temperature is required"}),400
    
    if not humidity:
        return jsonify({"message":"Humidity is required"}),400
    
    if not distance:
        return jsonify({"message":"Distance is required"}),400
    
    if not pressure:
        return jsonify({"message":"Pressure is required"}),400
    
    if not light_level:
        return jsonify({"message":"Light Level is required"}),400

    # validate if exist the sensor does not exist
    if c.execute("SELECT * FROM Sensor WHERE ID = ?",(sensor_id,)).fetchone() is None:
        return jsonify({"message":"Sensor does not exist"}),400

    c.execute("INSERT INTO Sensor_Data (sensor_id,time,temperature,humidity,distance,pressure,light_level) VALUES (?,?,?,?,?,?,?)",(sensor_id,time,temperature,humidity,distance,pressure,light_level))
    con.commit()
    con.close()
    return jsonify({"message":"Sensor data registered"}),201

# GET SENSOR DATA

@app.route('/sensor_data',methods=['GET'])
def get_sensor_data():
    con = connection()
    c = con.cursor()

    if not from_date:
        return jsonify({"message":"From date is required"}),400
    
    if not to_date:
        return jsonify({"message":"To date is required"}),400
    
    if not sensor_id:
        return jsonify({"message":"Sensor ID is required"}),400

    # validate if exist the sensor
    if c.execute("SELECT * FROM Sensor WHERE ID = ?",(sensor_id,)).fetchone() is None:
        return jsonify({"message":"Sensor does not exist"}),400

    c.execute("SELECT * FROM Sensor_Data WHERE sensor_id = ? AND time BETWEEN ? AND ?",(sensor_id,from_date,to_date))
    rows = c.fetchall()
    if rows is None:
        return jsonify({"message":"Sensor data not found"}),404
    con.close()
    return jsonify(rows)


if __name__ == "__main__":
    create_tables()
    app.run(debug=True,host='0.0.0.0')