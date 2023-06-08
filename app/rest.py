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
    c.execute("INSERT INTO Company (Company_Name,Company_API_Key) VALUES (?,?)",(company_name,company_api_key))
    if c.execute("SELECT * FROM Company WHERE Company_Name = ?",(company_name,)).fetchone() is not None:
        return jsonify({"message":"Company already exist"}),400
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
    Company = []
    for i in rows:
        get_Company = {}
        get_Company["ID"] = i["ID"]
        get_Company["Company_Name"] = i["Company_Name"]
        get_Company["Company_API_Key"] = i["Company_API_Key"]
        Company.append(get_Company)
    return jsonify(Company)


if __name__ == "__main__":
    create_tables()
    app.run(debug=True,host='0.0.0.0')