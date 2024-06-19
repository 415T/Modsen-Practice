from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = '86e33c67cbb59704738c0b3ff93f3afb'
BASE_URL_WEATHER = 'http://api.openweathermap.org/data/2.5/weather'
BASE_URL_AIR_POLLUTION = 'http://api.openweathermap.org/data/2.5/air_pollution'
BASE_URL_GEOCODING = 'http://api.openweathermap.org/geo/1.0/direct'
BASE_URL_WEATHER_MAPS = 'http://tile.openweathermap.org/map'


def make_request(url, params):
    try:
        response = requests.get(url, params=params)
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
    return make_request(BASE_URL_WEATHER, params)

@app.route('/weather/city/<city_name>', methods=['GET'])
def get_weather_by_city(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY
    }
    return make_request(BASE_URL_WEATHER, params)

@app.route('/weather/city_id/<int:city_id>', methods=['GET'])
def get_weather_by_city_id(city_id):
    params = {
        'id': city_id,
        'appid': API_KEY
    }
    return make_request(BASE_URL_WEATHER, params)

@app.route('/weather/zip', methods=['GET'])
def get_weather_by_zip():
    zip_code = request.args.get('zip')
    if not zip_code:
        return jsonify({'error': 'Missing required parameter: zip'}), 400

    params = {
        'zip': zip_code,
        'appid': API_KEY
    }
    return make_request(BASE_URL_WEATHER, params)

@app.route('/air_pollution', methods=['GET'])
def get_air_pollution():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing required parameters: lat and lon'}), 400

    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY
    }
    return make_request(BASE_URL_AIR_POLLUTION, params)

@app.route('/geocode', methods=['GET'])
def geocode():
    city_name = request.args.get('q')
    if not city_name:
        return jsonify({'error': 'Missing required parameter: q'}), 400

    params = {
        'q': city_name,
        'appid': API_KEY
    }
    return make_request(BASE_URL_GEOCODING, params)


@app.route('/weather_maps/<layer>/<int:z>/<int:x>/<int:y>', methods=['GET'])
def get_weather_maps(layer, z, x, y):

    valid_layers = ['clouds_new', 'precipitation_new', 'pressure_new', 'wind_new', 'temp_new']
    if layer not in valid_layers:
        return jsonify({'error': 'Invalid layer parameter'}), 400


    max_tile_number = (1 << z) - 1
    if z < 0 or z > 9 or x < 0 or x > max_tile_number or y < 0 or y > max_tile_number:
        return jsonify({'error': 'Invalid tile coordinates'}), 400

    url = f'{BASE_URL_WEATHER_MAPS}/{layer}/{z}/{x}/{y}.png'
    params = {
        'appid': API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.content, response.status_code, {'Content-Type': 'image/png'}
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
