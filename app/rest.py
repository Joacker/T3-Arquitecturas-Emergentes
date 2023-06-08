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
    con = connection()
    c = con.cursor()
    c.execute("Create table if not exists Admin (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT)")
    con.commit()
    c.execute("Insert into Admin (Username,Password) values ('admin','admin')")
    con.commit()
    c.execute("SELECT * FROM Admin")
    rows = c.fetchall()
    con.close()
    get_Admin = {}
    Admins = []
    for i in rows:
        get_Admin["ID"] = i["ID"] + 1
        get_Admin["Username"] = i["Username"]
        get_Admin["Password"] = i["Password"]
        Admins.append(get_Admin)
    return jsonify(Admins)



if __name__ == "__main__":
    create_tables()
    app.run(debug=True,host='0.0.0.0')