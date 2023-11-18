import threading
import requests
import time
import random
from datetime import datetime

# Define the base URL for the API
BASE_URL = 'http://server-container:5000'

NUM_THREADS = 3

SOFIA_CENTER = (42.6977, 23.3219)
SOFIA_RADIUS = 0.1


def create_car_and_add_location():
    car_id = random.randint(1, 1000)
    car = {
        'id': car_id,
        'locations': [{
            'coordinates': {
                'longitude': SOFIA_CENTER[1] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS),
                'latitude': SOFIA_CENTER[0] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS)
            },
            'timestamp': datetime.utcnow().isoformat(),
            'device_id': f'{car_id}'
        }]
    }
    # Send the POST request
    response = requests.post(f'{BASE_URL}/data/cars', json=car)
    if response.status_code == 200:
        print(f'Car created successfully with id {car_id}.')
    else:
        print(f'Error creating car with id {car_id}.')

    time.sleep(120)
    while True:
        location = {
            'coordinates': {
                'longitude': SOFIA_CENTER[1] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS),
                'latitude': SOFIA_CENTER[0] + random.uniform(-SOFIA_RADIUS, SOFIA_RADIUS)
            },
            'timestamp': datetime.utcnow().isoformat(),
            'device_id': f'{car_id}'
        }
        response = requests.post(f'{BASE_URL}/data/{location["device_id"]}', json=location)
        if response.status_code == 200:
            print(f'Location added successfully for car with id {car_id}.')
        else:
            print(f'Error adding location for car with id {car_id}.')
        time.sleep(120)


if __name__ == '__main__':
    time.sleep(20)
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=create_car_and_add_location)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
