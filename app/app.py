from flask import Flask
from flask_cors import CORS



app = Flask(__name__)
app.config['SECRET_KEY']='un_secreto_ssshhhhhh'
CORS(app)