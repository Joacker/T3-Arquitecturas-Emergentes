import os, jwt, bcrypt, datetime, logging, json
from flask import Flask, Blueprint, request, jsonify, g, session
from functools import wraps
from app import app
from Connect import connection
from werkzeug.exceptions import Unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app.secret_key = "un_secreto"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt1 = JWTManager(app)

# make decorator
def token_required_company(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token-company' in request.headers:
            token = request.headers['x-access-token-company']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_company = data['username']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_company, *args, **kwargs)
    return decorated

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
    
    password = generate_password_hash(password = password, method = 'sha256')
    
    c.execute("INSERT INTO Admin (Username, Password) VALUES (?, ?)", (username, password))
    con.commit()
    con.close()

    # Generate the access token using the username as a string
    # expire in 15 minutes
    access_token = create_access_token(identity={"username":username}, expires_delta=datetime.timedelta(minutes=15))

    return jsonify({"username": username, "access_token": access_token}), 200
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200    


@app.route("/login_company", methods=["POST"])
def login_company():
    con = connection()
    c = con.cursor()
    data = request.get_json()
    username = data['username']
    password = data['password']
    if not username:
        return jsonify({"message":"Username is required"}),400
    
    if not password:
        return jsonify({"message":"Password is required"}),400
    
    # validate if exist the company
    company = c.execute("SELECT * FROM Admin WHERE Username = ?",(username,)).fetchone()
    if company is None:
        return jsonify({"message":"Company not exist"}),400
    
    if not check_password_hash(company["Password"],password):
        return jsonify({"message":"Password is incorrect"}),400
    
    access_token = jwt.encode({"username":username}, app.config["SECRET_KEY"])
    #print(app.secret_key)
    con.close()
    return jsonify({"token":access_token,"message":"Login successfull"})

@app.route("/protected2", methods=["GET"])
@token_required_company
def protected2(current_company):
    return jsonify(logged_in_as=current_company), 200

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
    
    access_token = create_access_token(identity={"username":username}, expires_delta=datetime.timedelta(minutes=15))
    #print(app.secret_key)
    con.close()
    return jsonify({"token":access_token,"message":"Login successfull"})