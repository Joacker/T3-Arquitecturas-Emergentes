import os, jwt, bcrypt, datetime, logging, json
from flask import ( 
    Blueprint, request, jsonify, url_for, redirect, flash, session, g
    )
from Connect import connection
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message':'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            con = connection()
            c = con.cursor()
            c.execute("SELECT * FROM Admin WHERE Username = ?",(data['username'],))
            current_user = c.fetchone()
            con.close()
        except:
            return jsonify({'message':'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)