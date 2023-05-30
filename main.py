"""
    API REST con Python 3 y SQLite 3
    By Parzibyte: 
    ** https://parzibyte.me/blog **
"""
from flask import Flask, jsonify, request
from company_controller import create_company, create_location, create_sensor
from db import create_tables

app = Flask(__name__)

@app.route('/company', methods=['POST'])
def create_company_route():
    company_name = request.form.get('company_name')
    company_api_key = request.form.get('company_api_key')
    response = create_company(company_name, company_api_key)
    return jsonify(response)

@app.route('/location', methods=['POST'])
def create_location_route():
    company_id = request.form.get('company_id')
    location_name = request.form.get('location_name')
    location_country = request.form.get('location_country')
    location_city = request.form.get('location_city')
    location_meta = request.form.get('location_meta')
    response = create_location(company_id, location_name, location_country, location_city, location_meta)
    return jsonify(response)

@app.route('/sensor', methods=['POST'])
def create_sensor_route():
    location_id = request.form.get('location_id')
    sensor_id = request.form.get('sensor_id')
    sensor_name = request.form.get('sensor_name')
    sensor_category = request.form.get('sensor_category')
    sensor_meta = request.form.get('sensor_meta')
    sensor_api_key = request.form.get('sensor_api_key')
    response = create_sensor(location_id, sensor_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
    return jsonify(response)

if __name__ == '__main__':
    create_tables()
    """
    Here you can change debug and port
    Remember that, in order to make this API functional, you must set debug in False
    """
    app.run(host='0.0.0.0', port=8000, debug=False)