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
    c.execute("SELECT * FROM Location WHERE ID = ?",(id,))
    row = c.fetchone()
    if row is None:
        return jsonify({"message":"Location not found"}),404
    c.execute("DELETE FROM Location WHERE ID = ?",(id,))
    con.commit()
    con.close()
    return jsonify({"message":"Location deleted"})

if __name__ == "__main__":
    create_tables()
    app.run(debug=True,host='0.0.0.0')