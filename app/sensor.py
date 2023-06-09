from decorators import api_company_req, api_sensor_req, token_required
import os, jwt, bcrypt, datetime, logging, json
from flask import Flask, Blueprint, request, jsonify, g, session, make_response
from functools import wraps
from app import app
from Connect import connection
from flask_cors import CORS, cross_origin
from uuid import uuid4
# make route to insert in company table with protected route in token_required
CORS(app)

# GET SENSORS
@app.route('/api/v1/sensor/id',methods=['GET'])
@token_required
@api_company_req
def get_sensors(current_company_api_key,current_company_id,current_user):
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
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

    else:
        return make_response('company_id not match with company_api_key',  500)

# GET SENSOR BY ID
@app.route('/api/v1/sensor/id/',methods=['GET'])
@token_required
@api_company_req
def get_sensor(current_company_api_key,current_company_id,current_user):
    sensor_id = request.args.get('sensor_id')
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Sensor WHERE ID = "+sensor_id
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
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
        except:
            return make_response('Sensors not exist or id is invalid',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)

# REGISTER SENSOR
@app.route('/api/v1/insert_sensor',methods=['POST'])
@token_required
def register_sensor(current_user):
    con = connection()
    c = con.cursor()
    data = request.get_json()
    locationid = data['location_id']
    name = data['sensor_name']
    category = data['sensor_category']
    meta = data['sensor_meta']
    apikey = str(uuid4())

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
@app.route('/v1/sensor_update/',methods=['PUT'])
@token_required
def update_sensor(current_user):
    id = request.args.get('id')
    con = connection()
    c = con.cursor()
    data = request.get_json()
    locationid = data['location_id']
    name = data['sensor_name']
    category = data['sensor_category']
    meta = data['sensor_meta']

    if not locationid:
        return jsonify({"message":"Location ID is required"}),400
    
    if not name:
        return jsonify({"message":"Name is required"}),400
    
    if not category:
        return jsonify({"message":"Category is required"}),400
    
    if not meta:
        return jsonify({"message":"Meta is required"}),400

    # validate if exist the location does not exist
    if c.execute("SELECT * FROM Location WHERE ID = ?",(locationid,)).fetchone() is None:
        return jsonify({"message":"Location does not exist"}),400

    # validate if exist the sensor
    if c.execute("SELECT * FROM Sensor WHERE ID = ?",(id,)).fetchone() is None:
        return jsonify({"message":"Sensor does not exist"}),400
    
    c.execute("UPDATE Sensor SET location_id = ?, sensor_name = ?, sensor_category = ?, sensor_meta = ? WHERE ID = ?",(locationid,name,category,meta,id))
    con.commit()
    con.close()
    return jsonify({"message":"Sensor updated"})

# DELETE SENSOR
@app.route('/api/v1/sensor_delete',methods=['DELETE'])
@token_required
def delete_sensor(current_user):
    id = request.args.get('id')
    con = connection()
    c = con.cursor()
    if c.execute("SELECT * FROM Sensor WHERE ID = ?",(id,)).fetchone() is None:
        return jsonify({"message":"Sensor not found"}),404
        
    c.execute("DELETE FROM Sensor WHERE ID = ?",(id,))
    con.commit()
    con.close()
    return jsonify({"message":"Sensor deleted"})
