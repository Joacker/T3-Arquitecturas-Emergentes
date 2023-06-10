from crypt import methods
from app import app
from flask import jsonify, request, abort, make_response
from datetime import datetime
import jwt, json, sqlite3
from functools import wraps
from Connect import connection
from auth import *
from __init__db__ import create_tables

# from auth import token_required,api_company_req,api_sensor_req
# import Locations
# import Sensors
# import Sensors_data

#API's
@app.route('/',methods=['GET'])
def index():
    return jsonify({"message":"Welcome to the API"})

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