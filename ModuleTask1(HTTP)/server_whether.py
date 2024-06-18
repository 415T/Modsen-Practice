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


if __name__ == '__main__':
    app.run(debug=True)
