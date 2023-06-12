from decorators import api_company_req, api_sensor_req, token_required
import os, jwt, bcrypt, logging, json, time
from flask import Flask, Blueprint, request, jsonify, g, session, make_response
from functools import wraps
from app import app
from Connect import connection
from flask_cors import CORS, cross_origin
from ast import literal_eval
from datetime import datetime
# make route to insert in company table with protected route in token_required
CORS(app)

#REGISTER SENSOR DATA#
@app.route('/v1/sensor_data',methods=['POST'])
@token_required
@api_sensor_req
def send_data(current_sensor_api_key,current_sensor_id,current_user):
    json = request.json
    # extract sensor apikey from the header
    sensor_id  = json['sensor_id']
    # Getting the current date and time
    dt = datetime.now()
    # getting the timestamp
    time_epoch = datetime.timestamp(dt)
    humidity = json['humidity']
    temperature  = json['temperature']
    distance = json['distance']
    presure = json['presure']
    light_level = json['light_level']

    # extract from the header
    #sensor_api_key = request.headers.get('sensor_api_key')

    if int(current_sensor_id) == int(sensor_id):
        try:
            conn = connection()
            conn.execute("INSERT INTO Sensor_data (sensor_id, time, humidity, temperature, distance, pressure, light_level) VALUES (?,?,?,?,?,?,?)",(sensor_id,time_epoch,humidity,temperature,distance,presure,light_level))
            conn.commit()
            conn.close()
            resp = jsonify('Insert Sucefully')
            resp.status_code = 201  
            return resp
        except:
            resp = jsonify('Error in Insert Sensor')
            resp.status_code = 400  
            return resp
    else:
        resp = jsonify('Sensor id not match with sensor_api_key')
        resp.status_code = 400  
        return resp


# DELETE SENSOR DATA FOR ID
@app.route('/v1/sensor_data_delete',methods=['DELETE'])
@token_required
def delete_data(current_user):
    id = request.args.get('id')
    try:
        sql = f"DELETE FROM Sensor_data WHERE sensor_id={id}"
        conn = connection()
        conn.execute(sql)
        conn.commit()
        conn.close()
        return make_response('sensors data deleted',200)
    except:
        return make_response('sensors not exist or id is invalid',500,)

#GET SENSOR DATA
@app.route('/v1/sensor_data',methods=['GET'])
@token_required
@api_company_req
def get_data(current_company_api_key,current_company_id,current_user,):
    sensor_id = request.args.get('sensor_id')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    company_id = request.args.get('company_id')
    sensor_id_list = literal_eval(sensor_id)
    #counter = list()
    if int(current_company_id) == int(company_id):
        try:
            Sensors_data_collention = []
            for i in sensor_id_list:
                sql = f"SELECT * FROM Sensor_data Where sensor_id={i} and time BETWEEN {from_date} and {to_date}"
                conn = connection()
                rv = conn.execute(sql)
                rows = rv.fetchall()
                conn.close()

                Sensors_data_id = []
                #counter.append(sql)
                for j in rows:
                    sensors_data = {}
                    sensors_data["sensor_id "] = j["sensor_id"]
                    sensors_data["time"] = datetime.fromtimestamp(j["time"])
                    sensors_data["humidity"] = j["humidity"]
                    sensors_data["temperature "] = j["temperature"]
                    sensors_data["distance"] = j["distance"]
                    sensors_data["pressure"] = j["pressure"]
                    sensors_data["light_level"] = j["light_level"]
                    Sensors_data_id.append(sensors_data)
                Sensors_data_collention.append(Sensors_data_id)
                        

            resp = jsonify(Sensors_data_collention)
            resp.status_code = 201  
            return resp
        except:

            resp = jsonify('Error to obtain info of the Sensor ')
            resp.status_code = 400  
            return resp
    else:
        resp = jsonify('Company id not match with company_api_key ')
        resp.status_code = 400  
        return resp