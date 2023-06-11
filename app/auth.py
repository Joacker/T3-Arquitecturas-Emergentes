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
#from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

app.secret_key = "un_secreto"
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt1 = JWTManager(app)

# make decorator
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        current_user = {}
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, "un_secreto", verify=True, algorithms=['HS256'])
            user_t=data['user']
            sql = f"SELECT * FROM Admin WHERE Username='{user_t}'"
            conn = connection()
            rv = conn.execute(sql)
            rows = rv.fetchall()
            conn.close()
            for i in rows:
                current_user['username'] = i["Username"]
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)
        
    return decorator


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
    # auth from the body of the request
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
    
    sql = "SELECT * FROM Admin"
    conn = connection()
    rv = conn.execute(sql)
    rows = rv.fetchall()
    conn.close()
    for i in rows:
        user  = i  
    if user["Password"] == auth.password:  
        token = jwt.encode({'user': user["Username"]}, "un_secreto", algorithm='HS256')  
        return jsonify({'token' : token}) 
    
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route("/protected2", methods=["GET"])
@token_required
def protected2(current_user):
    return jsonify({"message":f"Hello {current_user['username']}"})

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
    
    # if not check_password_hash(admin["Password"], password):
    #     return jsonify({"message":"Password is incorrect"}),400
    
    if not admin["Password"] == password:
        return jsonify({"message":"Password is incorrect"}),400
    
    access_token = create_access_token(identity={"username":username}, expires_delta=datetime.timedelta(minutes=15))
    #print(app.secret_key)
    con.close()
    return jsonify({"token":access_token,"message":"Login successfull"})