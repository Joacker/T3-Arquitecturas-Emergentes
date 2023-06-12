from crypt import methods
from app import app
from flask import jsonify, request, abort, make_response
from datetime import datetime
import jwt, json, sqlite3
from functools import wraps
from Connect import connection
from auth import *
from __init__db__ import create_tables
import company, location, sensor, sensors_data
# from auth import token_required,api_company_req,api_sensor_req
# import Locations
# import Sensors
# import Sensors_data
from CORS import crossdomain
#API's
CORS(app)
@app.route('/',methods=['GET'])
def index():
    return jsonify({"message":"Welcome to the API"})

if __name__ == "__main__":
    create_tables()
    app.run(debug=True,host='0.0.0.0')