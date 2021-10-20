from flask import Blueprint, request
from utils import root_path
import os
from models.detection.yolo_f.tf2_keras_yolo3.object_detection import execute_object_dictation

ingredient = Blueprint('ingredient', __name__, url_prefix='/ingredient')


@ingredient.get('/')
def fetch_list():
    return f'fetch_list'


@ingredient.post('/detection')
def detection():
    base_path = os.path.join(root_path, 'models/detection/yolo_f/tf2_keras_yolo3')

    save_path = os.path.join(root_path, 'temp')
    img_path = os.path.join(root_path, 'temp/test.jpg')
    model_name = 'model_final.h5'

    img = request.files.get('image', '')
    img.save(img_path)

    execute_object_dictation(save_path, img_path, base_path, model_name)

    return f'detection'
