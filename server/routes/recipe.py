import os
from flask import Blueprint, request, jsonify
from models.recommenders.models.prediction_final import predictions

recipe = Blueprint('recipe', __name__, url_prefix='/recipe')

'''
theme_item: 카테고리를 골랐을때, 해당 카테고리의 레시피만 받아올 수 있음
idx2id: test_id를 조합으로 변경
idx2item: 결과를 이름으로 변환
item2idx: 카테고리에서 레시피 리스트를 가져오면, 레시피들을 숫자로 변환

파라미터: 조합아이디(test_id), 검색 카테고리에 해당하는 레시피 리스트(theme_item), 모델 경로(model_path)

1. 선호 요리 선택
2. 조합 아이디로 변경
3. 카테고리 선택
4. 카테고리에 해당하는 요리 리스트
'''


@recipe.post('/<type>/<page>')
def fetch_list(type, page):
    body = request.form

    ingredients = body.get('ingredients')
    categories = body.get('categories')

    model_path = 'models/recommenders/models/test_model.h5'
    user_id = [3]                       # 하나만 들어오면 요리 갯수 만큼 곱해주는 함수 위에 있음.
    item_id = [2, 6, 199, 235]          # 카테고리에 속한 요리 갯수 만큼 중복되지 않게 들어와야 함.
    recommends_top10 = predictions(user_id, item_id, model_path)
    return jsonify(recommends_top10)


@recipe.get('/<id>')
def fetch_detail(id):
    return f'fetch_detail {id}'


@recipe.post('/<id>')
def rating(id):
    body = request.form

    rating = body.get('rating')

    return f'rating {id} {rating}'
