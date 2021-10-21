from flask import Blueprint, request, send_file
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

    save_path = os.path.join(root_path, 'temp/detection.jpg')
    img_path = os.path.join(root_path, 'temp/smaple.jpg')
    model_name = 'model_final.h5'

    img = request.files.get('image', '')
    img.save(img_path)

    ingredients = execute_object_dictation(save_path, img_path, base_path, model_name)

    res = send_file(save_path, mimetype='image/jpeg', as_attachment=True)
    res.set_cookie('ingredients', ','.join(ingredients))

    # 디텍션 완료 후 삭제
    os.remove(img_path)
    os.remove(save_path)

    return res
