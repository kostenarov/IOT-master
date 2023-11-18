from flask import Flask, jsonify, request, render_template
import json
from geopy.distance import geodesic

app = Flask(__name__)

with open('data.json') as f:
    data = json.load(f)


@app.route('/')
def get_links():
    return render_template('index.html')


@app.route('/data/<int:car_id>', methods=['POST'])
def post_location(car_id):
    location = request.get_json()
    car = next((car for car in data['cars'] if car['id'] == car_id), None)
    if car:
        car['locations'].append(location)
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({'message': 'Location added successfully.'}), 200
    else:
        return jsonify({'error': 'Car not found.'}), 404


@app.route('/data/cars', methods=['POST'])
def post_car():
    car = request.get_json()
    data['cars'].append(car)
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({'message': 'Car added successfully.'}), 200


@app.route('/map/id/<int:car_id>')
def map(car_id):
    with open('data.json') as f:
        data = json.load(f)
    coordinates = []
    for car in data['cars']:
        if car['id'] == car_id:
            coordinates = [location['coordinates'] for location in car['locations']]
            print(coordinates)
            break

    if len(coordinates) == 0:
        return jsonify({'error': 'Car not found.'}), 404
    return render_template('map.html', coordinates=coordinates)


@app.route('/map/latest')
def get_latest_map():
    latest_locations = []
    for car in data['cars']:
        if car['locations']:
            latest_location = max(car['locations'], key=lambda x: x['timestamp'])
            latest_locations.append({'latitude': latest_location['coordinates']['latitude'],
                                     'longitude': latest_location['coordinates']['longitude']})
    if len(latest_locations) == 0:
        return jsonify({'error': 'Cars not found.'}), 404
    return render_template('map.html', coordinates=latest_locations)


@app.route('/map/furthest')
def get_furthest_map():
    reference_location = (42.65234964884238, 23.354063873748185)
    furthest_locations = []
    for car in data['cars']:
        furthest_location = max(car['locations'], key=lambda x: geodesic(reference_location, (
        x['coordinates']['latitude'], x['coordinates']['longitude'])).km)
        furthest_locations.append({'latitude': furthest_location['coordinates']['latitude'],
                                   'longitude': furthest_location['coordinates']['longitude']})
    if len(furthest_locations) == 0:
        return jsonify({'error': 'Cars not found.'}), 404
    return render_template('map.html', coordinates=furthest_locations)


if __name__ == '__main__':
    app.run(debug=True)
