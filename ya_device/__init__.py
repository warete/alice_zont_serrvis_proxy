import requests
import datetime

API_URL = 'https://api.iot.yandex.net'
CHANGE_STATE_METHOD = '/v1.0/devices/actions'
CHANGE_GET_STATE_METHOD = '/v1.0/devices/'


def change_state(token, device_id, state):
    response = requests.post(
        API_URL + CHANGE_STATE_METHOD,
        json={
            "devices": [
                {
                    "id": device_id,
                    "actions": [
                        {
                            "type": "devices.capabilities.on_off",
                            "state": {
                                "instance": "on",
                                "value": state
                            }
                        }
                    ]
                }
            ]
        },
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response.json()


def get_state(token, device_id):
    response = requests.get(
        API_URL + CHANGE_GET_STATE_METHOD + device_id,
        headers={
            "Content-type": "application/json",
            "Authorization": "Bearer " + token
        }
    )

    return response.json()
