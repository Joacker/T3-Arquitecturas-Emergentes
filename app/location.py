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
@app.route('/v1/get_locations',methods=['GET'])
@token_required
@api_company_req
def getM_locations(current_company_api_key,current_company_id,current_user):
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Location"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            loactions = []
            for i in rows:
                    location = {}
                    location["company_id "] = i["company_id"]
                    location["location_name "] = i["location_name"]
                    location["location_country "] = i["location_country"]
                    location["location_city"] = i["location_city"]
                    location["location_meta"] = i["location_meta"]
                    loactions.append(location)
            
            return jsonify(loactions)
            
        except:
            return make_response('Locations not exist',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)


# GET LOCATION BY ID
@app.route('/v1/get_locations/id/',methods=['GET'])
@token_required
@api_company_req
def getU_location(current_company_api_key,current_company_id,current_user):
    location_id = request.args.get('location_id')
    company_id = request.args.get('company_id')
    if int(current_company_id) == int(company_id):
        try:
            sql = "SELECT * FROM Location Where ID="+location_id
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            loactions = []
            for i in rows:
                    location = {}
                    location["company_id "] = i["company_id"]
                    location["location_name "] = i["location_name"]
                    location["location_country "] = i["location_country"]
                    location["location_city"] = i["location_city"]
                    location["location_meta"] = i["location_meta"]
                    loactions.append(location)

            return jsonify(loactions)
        except:
            return make_response('Locations not exist or id is invalid',  500)
    else:
        return make_response('company_id not match with company_api_key',  500)

# UPDATE LOCATION
@app.route('/v1/get_locations',methods=['PUT'])
@token_required
def update_location(current_user):
    id = request.args.get('id')
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
@app.route('/v1/get_locations',methods=['DELETE'])
@token_required
def delete_location(current_user):
    id = request.args.get('id')
    con = connection()
    c = con.cursor()

    # validate if exist the location
    if c.execute("SELECT * FROM Location WHERE ID = ?",(id,)).fetchone() is None:
        return jsonify({"message":"Location does not exist"}),400
    
    c.execute("DELETE FROM Location WHERE ID = ?",(id,))
    con.commit()
    con.close()
    return jsonify({"message":"Location deleted"})

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