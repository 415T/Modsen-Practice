import pytest
from flask import Flask
from server_whether import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_weather_by_city(client):
    response = client.get('/weather/city/London')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_get_weather_by_city_id(client):
    response = client.get('/weather/city_id/2172797')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_get_weather_by_coordinates(client):
    response = client.get('/weather/coordinates?lat=35&lon=139')
    assert response.status_code == 307
    redirect_response = client.get(response.headers['Location'])
    assert redirect_response.status_code == 200
    data = redirect_response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_get_weather_by_lat_lon(client):
    response = client.get('/weather/lat_lon?lat=35&lon=139')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_get_weather_by_zip(client):
    response = client.get('/weather/zip?zip=94040')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_get_air_pollution(client):
    response = client.get('/air_pollution?lat=35&lon=139')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_geocode(client):
    response = client.get('/geocode?q=London')
    assert response.status_code == 200
    data = response.get_json()
    assert 'status_code' in data
    assert 'data' in data

def test_get_weather_maps(client):
    response = client.get('/weather_maps/clouds_new/3/4/2')
    assert response.status_code == 200
    assert response.data
    assert response.headers['Content-Type'] == 'image/png'

def test_invalid_layer(client):
    response = client.get('/weather_maps/invalid_layer/3/4/2')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_invalid_coordinates(client):
    response = client.get('/weather_maps/clouds_new/10/1024/1024')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    response = client.get('/weather_maps/clouds_new/3/10/10')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_missing_parameters(client):
    response = client.get('/weather/coordinates')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    response = client.get('/weather/zip')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    response = client.get('/air_pollution')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    response = client.get('/geocode')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

    response = client.get('/weather_maps/clouds_new/3/10/10')
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
