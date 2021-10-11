from flask import Blueprint, jsonify

category = Blueprint('category', __name__, url_prefix='/category')


@category.get('/')
def fetch_list():
    return jsonify(['카테고리', '리스트', 'test'])
