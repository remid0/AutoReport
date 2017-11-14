from datetime import datetime

import requests

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

# Examples of GPS coordinates
    # 49.42043, 2.79502 : N31
    # 49.41271, 2.81436 : Boulevard
    # 49.4183, 2.6944 : Autoroute du Nord
    # 49.04874, 2.09101 : Rue des Marechaux
    # 49.04851, 2.09222 : Rue des Marechaux

payload = [{
    'car': 411332767,  # Car vin code: 411332767 | 142897311
    'start_date': datetime.utcnow().strftime(DATETIME_FORMAT),
    'stop_date': datetime.now().strftime(DATETIME_FORMAT),
    'mode': 'AUT',  # Mode as three letter code
    'distance': 20,
    'users': [3, 4],  # List of User server ids
    'gps_points': [
        {
            'datetime': datetime.utcnow().strftime(DATETIME_FORMAT),
            'latitude': 49.42043,
            'longitude': 2.79502,
            'altitude': 0,
            'speed': 15,
            'track': 26,
        },
    ]
}]

result = requests.post('http://localhost:8000/sessions/create/', json=payload)

if result.status_code != 201:
    raise ValueError('Failed to updload data')
