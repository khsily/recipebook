from flask import Blueprint, request
from utils import root_path
import os

ingredient = Blueprint('ingredient', __name__, url_prefix='/ingredient')


@ingredient.get('/')
def fetch_list():
    return f'fetch_list'


@ingredient.post('/detection')
def detection():
    img = request.files.get('image', '')
    path = os.path.join(root_path, 'data/test.jpg')
    img.save(path)
    return f'detection'
