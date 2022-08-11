import requests
import datetime

API_URL = 'https://zont-online.ru/api/load_data'


def get_data(login, password, email, device_id):
    current_time = int(datetime.datetime.now().timestamp())
    response = requests.post(
        API_URL,
        json={
            "requests": [
                {
                    "device_id": device_id,
                    "data_types": ["thermostat_work"],
                    "mintime": current_time - 60,
                    "maxtime": current_time
                }
            ]
        },
        headers={
            "X-ZONT-Client": email,
            "Content-type": "application/json"
        },
        auth=(login, password)
    )

    return response.json()
