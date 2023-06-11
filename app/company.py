from decorators import token_required, api_company_req, api_sensor_req
import os, jwt, bcrypt, datetime, logging, json
from flask import Flask, Blueprint, request, jsonify, g, session, make_response
from functools import wraps
from app import app
from Connect import connection

# Get Company
@app.route('/get_company',methods=['GET'])
def get_company():
    con = connection()
    c = con.cursor()
    c.execute("SELECT * FROM Company")
    rows = c.fetchall()
    con.close()
    Company = []
    for i in rows:
        get_Company = {}
        get_Company["ID"] = i["ID"]
        get_Company["Company_Name"] = i["Company_Name"]
        get_Company["Company_API_Key"] = i["Company_API_Key"]
        Company.append(get_Company)
    return jsonify(Company)


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
