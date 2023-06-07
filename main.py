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
    if not company_name or not company_api_key:
        return jsonify({"error": "Invalid input data"}), 400
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

#La inserción de sensor_data debe tener la siguiente estructura:
# POST /api/v1/sensor_data
# Insertar datos ocupando el sensor_api_key como mecanismo de autorización.
# Debe retornar Status HTTP 201 (created).
@app.route('/sensor', methods=['POST'])
def create_sensor_route():
    location_id = request.form.get('location_id')
    sensor_name = request.form.get('sensor_name')
    sensor_api_key = request.form.get('sensor_api_key')
    response = create_sensor(location_id, sensor_name, sensor_api_key)
    return jsonify(response)

#La consulta de sensor_data debe tener la siguiente estructura:
# GET /api/v1/sensor_data
# Parámetros requeridos:
# La autorización será posible mediante el uso de un Header HTTP o puede tener un parámetro en la URL &company_api_key= from = < marca de tiempo en formato EPOCH > to = < marca de tiempo en formato EPOCH > sensor_id = [2,3,4,5,10,220] (Arreglo de sensor_id para los cuales se consultan los sensor_data)
@app.route('/sensor_data', methods=['GET'])
def get_sensor_data():
    return jsonify({})


if __name__ == '__main__':
    create_tables()
    """
    Here you can change debug and port
    Remember that, in order to make this API functional, you must set debug in False
    """
    app.run(host='0.0.0.0', port=8000, debug=False)