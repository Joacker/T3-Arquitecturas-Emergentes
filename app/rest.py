from flask import jsonify
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
    
    Locations = [{'ID': i['ID'], 'NAME': i['NAME'], 'LATITUDE': i['LATITUDE'], 'LONGITUDE': i['LONGITUDE']} for i in rows]
    return jsonify(Locations)

# GET LOCATION BY ID
@app.route('/locations/<int:id>',methods=['GET'])
def get_location(id):
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Location WHERE ID = ?",(id,))
    row = c.fetchone()
    con.close()
    if row is None:
        return jsonify({"message":"Location not found"}),404
    get_Location = {}
    get_Location["ID"] = row["ID"]
    get_Location["NAME"] = row["NAME"]
    get_Location["LATITUDE"] = row["LATITUDE"]
    get_Location["LONGITUDE"] = row["LONGITUDE"]
    return jsonify(get_Location)

# REGISTER LOCATION
@app.route('/locations',methods=['POST'])
def register_location():
    con = connection()
    c = con.cursor()
    data = request.get_json()
    id = data['ID']
    companyid = data['COMPANY_ID']
    name = data['LOCATION_NAME']
    country = data['LOCATION_COUNTRY']
    city = data['LOCATION_CITY']
    meta = data['LOCATION_META']

    if not id:
        return jsonify({"message":"ID is required"}),400
    
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
    
    # validate if exist the location
    if c.execute("SELECT * FROM Location WHERE ID = ?",(id,)).fetchone() is not None:
        return jsonify({"message":"Location already exist"}),400
    
    c.execute("INSERT INTO Location (ID,COMPANY_ID,NAME,COUNTRY,CITY,META) VALUES (?,?,?,?,?,?)",(id,companyid,name,country,city,meta))
    con.commit()
    con.close()
    return jsonify({"message":"Location created"})


# UPDATE LOCATION
@app.route('/locations/<int:id>',methods=['PUT'])
def update_location(id):
    con = connection()
    c = con.cursor()
    data = request.get_json()
    name = data['name']
    latitude = data['latitude']
    longitude = data['longitude']
    
    if not name:
        return jsonify({"message":"Name is required"}),400
    
    if not latitude:
        return jsonify({"message":"Latitude is required"}),400
    
    if not longitude:
        return jsonify({"message":"Longitude is required"}),400
    
    # validate if exist the location
    if c.execute("SELECT * FROM Locations WHERE Name = ?",(name,)).fetchone() is not None:
        return jsonify({"message":"Location already exist"}),400
    
    c.execute("UPDATE Locations SET Name = ?,Latitude = ?,Longitude = ? WHERE ID = ?",(name,latitude,longitude,id))
    con.commit()
    con.close()
    return jsonify({"message":"Location updated"})

# DELETE LOCATION
@app.route('/locations/<int:id>',methods=['DELETE'])
def delete_location(id):    
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Locations WHERE ID = ?",(id,))
    row = c.fetchone()
    if row is None:
        return jsonify({"message":"Location not found"}),404
    c.execute("DELETE FROM Locations WHERE ID = ?",(id,))
    con.commit()
    con.close()
    return jsonify({"message":"Location deleted"})

if __name__ == "__main__":
    create_tables()
    app.run(debug=True,host='0.0.0.0')