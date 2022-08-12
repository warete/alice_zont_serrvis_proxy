import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import atexit
import time
import win32gui, win32con


import zont
import ya_device
import utils

load_dotenv()

hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hide, win32con.SW_HIDE)

zont_params = {
    'device_id': os.getenv('ZONT_DEVICE_ID'),
    'email': os.getenv('ZONT_EMAIL'),
    'login': os.getenv('ZONT_LOGIN'),
    'password': os.getenv('ZONT_PASSWORD'),
}

# Номер зоны => id розетки в яндексе
zone_to_ya_device = {
    '4': os.getenv('ZONE_4_DEVICE_ID'),
}

YA_CLIENT_ID = str(os.getenv('YA_CLIENT_ID'))


def check_them_zones():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    token = utils.get_token()

    if token is False:
        print('Без токена работа невозможна')
        # todo: send notification
        return

    response = zont.get_data(zont_params['login'], zont_params['password'], zont_params['email'],
                             zont_params['device_id'])

    if response:
        zones_data = response['responses'][0]['thermostat_work']['zones']
        for zone_number, item in zones_data.items():
            worktime = item['worktime'][0][1]
            print('Зона #{}, время работы {} сек'.format(zone_number, worktime))
            if zone_number in zone_to_ya_device:
                state = False if worktime < 60 else True
                # Получаем текущее состояние устройств
                current_state_response = ya_device.get_state(token, zone_to_ya_device[zone_number])
                # Меняем состояние только если новое отличается от текущего
                if current_state_response['capabilities'][0]['state']['value'] != state:
                    print('alice item state change to', 'on' if state else 'off')
                    ya_device.change_state(token, zone_to_ya_device[zone_number], state)
    else:
        print('Error: ', response)


scheduler = BackgroundScheduler()
scheduler.add_job(func=check_them_zones, trigger="interval", seconds=5)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

app = Flask(__name__)


@app.route("/")
def main_action():
    auth_link = 'https://oauth.yandex.ru/authorize?response_type=token&client_id=' + YA_CLIENT_ID
    return 'Для авторизации в приложении через Яндекс нужно перейти по ссылке <a href="{}">{}</a>'.format(auth_link,
                                                                                                          auth_link)


@app.route("/set_token")
def set_token_action():
    return '''
    <script>
        var token = /access_token=([^&]+)/.exec(document.location.hash)[1];
        window.location = "/app_response_token/" + token;
        </script>
    '''


@app.route('/app_response_token/<token>/', methods=['GET'])
def app_response_token_action(token):
    utils.write_token(token)
    return 'Токен сохранен в файл {}'.format(utils.get_token_path())


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, port=3000, host='0.0.0.0')
