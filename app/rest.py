from crypt import methods
import sqlite3
from app import app
from flask import jsonify, request,abort,make_response
from datetime import datetime
import jwt
from functools import wraps
from Connect import connection
import json

# from auth import token_required,api_company_req,api_sensor_req
# import Locations
# import Sensors
# import Sensors_data

#API's

#API's de Usuarios
# @app.route('/api/v1/login',methods=['POST'])
# def login_user():
#     auth = request.authorization
#     if not auth or not auth.username or not auth.password:
#         return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})    

#     sql = "SELECT * FROM Admin"
#     conn = connection()
#     rv = conn.execute(sql)
#     rows = rv.fetchall()
#     conn.close()
#     for i in rows:
#         user  = i  
#     if user["Password"] == auth.password:  
#         token = jwt.encode({'user': user["Username"]}, app.config['SECRET_KEY'], algorithm='HS256')  
#         return jsonify({'token' : token}) 
    
#     return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


# @app.route('/api/v1/user')
# @token_required
# def get_user(current_user):
#     sql = "SELECT * FROM Admin"
#     conn = connection()
#     rv = conn.execute(sql)
#     rows = rv.fetchall()
#     conn.close()
#     user = {}
#     for i in rows:
            
#             user["User"] = i["Username"]
#             user["Pass"] = i["Password"]

#     return jsonify(user)

# #API's de Compnay
# @app.route('/api/v1/company',methods=['GET'])
# @token_required
# def get_company(current_user):
#     try:
#         sql = "SELECT * FROM Company"
#         conn = connection()
#         rv = conn.execute(sql)
#         rows = rv.fetchall()
#         conn.close()
#         companys = []
#         company = {}
#         for i in rows:
#                 company["ID "] = i["ID"]
#                 company["company_name"] = i["company_name"]
#                 company["company_api_key"] = i["company_api_key"]
#                 companys.append(company)

#         return jsonify(companys)
#     except:
#         return make_response('Companys not exist',  500)


@app.route('/',methods=['GET'])
def index():
    con = connection()
    c = con.cursor()
    c.execute("Create table if not exists Admin (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)")
    c.execute("Create table if not exists Company (ID INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, company_api_key TEXT)")
    c.execute("Create table if not exists Locations (ID INTEGER PRIMARY KEY AUTOINCREMENT, company_id INTEGER, location_name TEXT, location_api_key TEXT)")
    c.execute("Create table if not exists Sensors (ID INTEGER PRIMARY KEY AUTOINCREMENT, location_id INTEGER, sensor_name TEXT, sensor_api_key TEXT)")
    c.execute("Create table if not exists Sensors_data (ID INTEGER PRIMARY KEY AUTOINCREMENT, sensor_id INTEGER, sensor_data TEXT, sensor_date TEXT)")
    con.commit()
    c.execute("Insert into Admin (Username,Password) values ('admin','admin')")
    con.commit()
    c.execute("SELECT * FROM Admin")
    rows = c.fetchall()
    con.close()
    get_Admin = {}
    Admins = []
    for i in rows:
        get_Admin["ID"] = i["ID"]
        get_Admin["Username"] = i["Username"]
        get_Admin["Password"] = i["Password"]
        Admins.append(get_Admin)
    return jsonify(Admins)
    




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')