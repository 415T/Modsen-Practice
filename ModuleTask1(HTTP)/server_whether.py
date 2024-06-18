from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = '86e33c67cbb59704738c0b3ff93f3afb'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


def make_request(params):
    try:
        response = requests.get(BASE_URL, params=params)
        status_code = response.status_code
        data = response.json()

        return jsonify({
            'status_code': status_code,
            'data': data
        }), status_code
    except requests.exceptions.RequestException as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/weather/coordinates', methods=['GET'])
def get_weather_by_coordinates():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing required parameters: lat and lon'}), 400

    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY
    }
    return make_request(params)

@app.route('/weather/city/<city_name>', methods=['GET'])
def get_weather_by_city(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY
    }
    return make_request(params)

@app.route('/weather/city_id/<int:city_id>', methods=['GET'])
def get_weather_by_city_id(city_id):
    params = {
        'id': city_id,
        'appid': API_KEY
    }
    return make_request(params)

@app.route('/weather/zip', methods=['GET'])
def get_weather_by_zip():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({'error': 'Missing required parameter: zip'}), 400

    params = {
        'zip': zip_code,
        'appid': API_KEY
    }
    return make_request(params)


if __name__ == '__main__':
    app.run(debug=True)
