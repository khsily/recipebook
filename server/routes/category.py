from flask import Blueprint, jsonify
import db

category = Blueprint('category', __name__, url_prefix='/category')


@category.get('/')
def fetch_list():
    res = db.execute('fetchCategory.sql')
    return jsonify(res)
