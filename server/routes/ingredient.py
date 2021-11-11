from flask import Blueprint, request, send_file
from flask.json import jsonify
from utils import root_path
import os
import json
import db
import uuid

from models.detection.yolo_f.tf2_keras_yolo3.object_detection_yolo_v4 import load_model, predict

base_path = os.path.join(root_path, 'models/detection/yolo_f/tf2_keras_yolo3')
model_path = os.path.join(base_path, 'model_yolov4.h5')
model = load_model(model_path)

ingredient = Blueprint('ingredient', __name__, url_prefix='/ingredient')


@ingredient.get('/')
def fetch_list():
    ingredients = db.execute('fetchIngredient.sql', {'ingredients': None})
    return jsonify(ingredients)


@ingredient.post('/detection')
def detection():
    unique_id = uuid.uuid4()

    class_path = os.path.join(base_path, 'model_data/recipebook.korean.names')
    save_path = os.path.join(root_path, f'temp/detection_{unique_id}.jpg')
    img_path = os.path.join(root_path, f'temp/smaple_{unique_id}.jpg')

    img = request.files.get('image', '')
    img.save(img_path)

    ingredients = predict(model, class_path, img_path, save_path)
    ingredients = json.dumps(','.join(list(ingredients)))

    res = send_file(save_path, mimetype='image/jpeg', as_attachment=True)
    res.set_cookie('ingredients', ingredients)

    print(unique_id, flush=True)
    print('^^' * 10, flush=True)

    # 디텍션 완료 후 삭제
    os.remove(img_path)
    os.remove(save_path)

    return res
