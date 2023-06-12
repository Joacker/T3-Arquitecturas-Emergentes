import os, jwt, bcrypt, datetime, logging, json
from flask import Flask, Blueprint, request, jsonify, g, session, make_response
from functools import wraps
from app import app
from Connect import connection
from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from decorators import token_required, api_company_req, api_sensor_req
app.secret_key = "un_secreto"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt1 = JWTManager(app)

#GET ADMINS
@app.route('/get_admin', methods=['GET'])
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
@app.route('/register', methods=['POST'])
def register_admin():
    con = connection()
    c = con.cursor()
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"message": "Username is required"}), 400

    if not password:
        return jsonify({"message": "Password is required"}), 400

    # validate if admin exists
    if c.execute("SELECT * FROM Admin WHERE Username = ?", (username,)).fetchone() is not None:
        return jsonify({"message": "Admin already exists"}), 400
    
    #password = generate_password_hash(password = password, method = 'sha256')
    
    c.execute("INSERT INTO Admin (Username, Password) VALUES (?, ?)", (username, password))
    con.commit()
    con.close()

    return jsonify("Welcome ",username), 200 

#LOGIN USER
@app.route('/login',methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    con = connection()
    c = con.cursor()
    if not username:
        return jsonify({"message": "Username is required"}), 400
    if not password:
        return jsonify({"message": "Password is required"}), 400
    # validate if admin exists
    if c.execute("SELECT * FROM Admin WHERE Username = ?", (username,)).fetchone() is None:
        return jsonify({"message": "Admin does not exist"}), 400
    # validate password
    if not password == c.execute("SELECT * FROM Admin WHERE Username = ?", (username,)).fetchone()["Password"]:
        return jsonify({"message": "Password is incorrect"}), 400
    
    token = jwt.encode({'user': username}, "un_secreto", algorithm='HS256')  
    return jsonify({'token' : token}) 
    
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})