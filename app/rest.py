from crypt import methods
import sqlite3
from app import app
from flask import jsonify, request,abort,make_response
from datetime import datetime
import jwt
from functools import wraps
from Connect import connection

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
    return jsonify({'message': 'Welcome to the API'})




if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')