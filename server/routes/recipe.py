import os
import json
from flask import Blueprint, request, jsonify
from models.recommenders.models.prediction_final import predictions
import db

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


# 추천 리스트
@recipe.post('/recommend/<page>')
def fetch_recommend(page):
    body = request.form
    favors = body.get('favors') or '[]'  # TODO: favors 사용

    model_path = 'models/recommenders/models/test_model.h5'
    user_id = [3]                       # 하나만 들어오면 요리 갯수 만큼 곱해주는 함수 위에 있음.
    item_id = [2, 6, 199, 235]          # 카테고리에 속한 요리 갯수 만큼 중복되지 않게 들어와야 함.
    recommends_top10 = predictions(user_id, item_id, model_path)

    return jsonify(recommends_top10)


# 검색 (검색 리스트 + 추천 리스트)
@recipe.post('/<page>')
def fetch_list(page):
    body = request.form
    ingredients = body.get('ingredients') or '[]'
    categories = body.get('categories') or '[]'
    favors = body.get('favors') or '[]'  # TODO: favors 사용

    num_per_page = 20
    offset = (int(page) - 1) * num_per_page
    limit = offset + num_per_page

    # 값이 존재하면 list로, 없으면 None(전체선택)으로
    ingredients = json.loads(ingredients) or None
    categories = json.loads(categories) or None

    recipes = db.execute('fetchRecipeList.sql', {
        'categories': categories,
        'ingredients': ingredients,
        'limit': limit,
        'offset': offset,
    })

    return jsonify(recipes)


@recipe.get('/<id>')
def fetch_detail(id):
    # view count 올리기
    db.update('updateRecipeView.sql', {'id': id})

    # detail, ingredients, steps 합치기
    detail = db.execute('fetchRecipeDetail.sql', {'id': id})
    ingredients = db.execute('fetchRecipeIngredient.sql', {'id': id})
    steps = db.execute('fetchRecipeStep.sql', {'id': id})

    detail = detail and dict(detail[0])
    detail['ingredients'] = ingredients
    detail['steps'] = steps

    return jsonify(detail)


@recipe.post('/<id>')
def rating(id):
    body = request.form

    rating = body.get('rating')

    return f'rating {id} {rating}'
