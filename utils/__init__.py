from pathlib import Path
import os


def get_token_path():
    return os.path.join(str(Path.home()), 'zont_thermo_proxy_token.txt')


def write_token(token):
    try:
        with open(get_token_path(), 'w') as file:
            file.write(token)

    except FileNotFoundError:
        print("Невозможно открыть файл" + get_token_path())


def get_token():
    try:
        with open(get_token_path(), 'r') as file:
            return file.readline()

    except FileNotFoundError:
        print("Невозможно открыть файл" + get_token_path())
        return False
