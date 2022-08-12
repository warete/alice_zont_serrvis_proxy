from pathlib import Path
import os


def get_work_path():
    return os.path.join(str(Path.home()), 'zont_thermo_proxy')


def check_work_dir():
    path = Path(get_work_path())
    path.mkdir(parents=True, exist_ok=True)


def get_token_path():
    return os.path.join(get_work_path(), 'zont_thermo_proxy_token.txt')


def get_logs_path():
    return os.path.join(get_work_path(), 'main.log')


def write_token(token, logger):
    try:
        with open(get_token_path(), 'w') as file:
            file.write(token)

    except FileNotFoundError:
        logger.error("Невозможно открыть файл" + get_token_path())


def get_token(logger):
    try:
        with open(get_token_path(), 'r') as file:
            return file.readline()

    except FileNotFoundError:
        logger.error("Невозможно открыть файл" + get_token_path())
        return False
