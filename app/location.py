from decorators import api_company_req, api_sensor_req, token_required
import os, jwt, bcrypt, datetime, logging, json
from flask import Flask, Blueprint, request, jsonify, g, session, make_response
from functools import wraps
from app import app
from Connect import connection
from flask_cors import CORS, cross_origin
# make route to insert in company table with protected route in token_required
CORS(app)

# GET LOCATIONS
@app.route('/get_locations',methods=['GET'])
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


# REGISTER LOCATION
@app.route('/v1/create_location',methods=['POST'])
@token_required
def register_location(current_user):
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