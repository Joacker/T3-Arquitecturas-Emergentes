from decorators import api_company_req, api_sensor_req, token_required
import os, jwt, bcrypt, datetime, logging, json
from flask import Flask, Blueprint, request, jsonify, g, session, make_response
from functools import wraps
from app import app
from Connect import connection
from flask_cors import CORS, cross_origin
# make route to insert in company table with protected route in token_required
CORS(app)

@app.route("/create_company", methods=["POST"])
@token_required
def insert_company(current_user):
    company_name = request.json['company_name']
    company_api_key = request.json['company_api_key']
    # insert data in the company table
    sql = "INSERT INTO Company (company_name, company_api_key) VALUES (?, ?)"
    conn = connection()
    conn.execute(sql, (company_name, company_api_key))
    conn.commit()
    conn.close()
    return jsonify({"message": company_name})


@app.route("/get_company", methods=["GET"])
def get_company():
    # get all data from company table
    sql = "SELECT * FROM Company"
    conn = connection()
    rv = conn.execute(sql)
    rows = rv.fetchall()
    conn.close()
    Companies = []
    for i in rows:
        get_Admin = {}
        get_Admin["ID"] = i["ID"]
        get_Admin["company_name"] = i["company_name"]
        get_Admin["company_api_key"] = i["company_api_key"]
        Companies.append(get_Admin)
    return jsonify(Companies)


@app.route("/login_company", methods=["POST"])
def login_company():
    # auth from the body of the request
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
    sql = "SELECT * FROM Admin"
    conn = connection()
    rv = conn.execute(sql)
    rows = rv.fetchall()
    conn.close()
    for i in rows:
        user  = i  
    if user["Password"] == auth.password:  
        token = jwt.encode({'user': user["Username"]}, "un_secreto", algorithm='HS256')  
        return jsonify({'token' : token}) 
    
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route("/protected2", methods=["GET"])
@token_required
def protected2(current_user):
    return jsonify({"message":f"Hello {current_user['username']}"})
