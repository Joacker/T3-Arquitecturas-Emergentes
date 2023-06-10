import os, jwt, bcrypt, datetime
import logging, json
from flask import Flask, Blueprint, request, jsonify, g, session
from functools import wraps
from Connect import connection
from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_user_id():
    token = request.headers.get('X-Auth-Token')
    if not token:
        logging.info("Missing authorized header")
        raise Unauthorized('Missing  authorized header')
    try:
        payload = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=["HS256"])
        
    except jwt.exceptions.DecodeError:
        raise Unauthorized('Invalid authorization token from user')

def monitoring(response):
    fecha = datetime.datetime.utcnow()
    try:
        usuario_id = get_user_id()
    except Unauthorized:
        usuario_id = -1

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
    password = generate_password_hash(password)
    
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


#LOGIN ADMIN
@app.route('/login',methods=['POST'])
def login():
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
    admin = c.execute("SELECT * FROM Admin WHERE Username = ?",(username,)).fetchone()
    if admin is None:
        return jsonify({"message":"Admin not exist"}),400
    
    if not check_password_hash(admin["Password"],password):
        return jsonify({"message":"Password is incorrect"}),400
    
    token = jwt.encode({"id":admin["username"],"exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},os.environ['SECRET_KEY'],algorithm="HS256")
    con.close()
    return jsonify({"token":token})
