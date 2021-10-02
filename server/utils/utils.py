import pathlib
import os

root_path = pathlib.Path().resolve()


def is_dev():
    return os.environ['FLASK_ENV'] == 'development'
