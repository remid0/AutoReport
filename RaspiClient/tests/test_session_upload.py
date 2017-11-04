from datetime import datetime

import requests

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


payload = [{
    'start_date': datetime.utcnow().strftime(DATETIME_FORMAT),
    'stop_date': datetime.now().strftime(DATETIME_FORMAT),
    'mode': 'AUT',
    'distance': 20,
    'users': [1, 2],  # it's an id from django store as server_pk in local database
    'gps_traces': [
        {
            'datetime': datetime.utcnow().strftime(DATETIME_FORMAT),
            'latitude': 10,
            'longitude': 10,
            'altitude': 10,
        },
    ]
}]

result = requests.post('http://localhost:8000/sessions/create/', json=payload)

if result.status_code != 201:
    raise ValueError('Failed to updload data')
