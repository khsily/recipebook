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


def get_recommend_ids(id, top_n):
    if not id:
        return None

    recipe_ids = db.execute('fetchAllRecipeIds.sql')
    recipe_ids = [recipe['id'] for recipe in recipe_ids]

    model_path = 'models/recommenders/models/test_model.h5'
    user_id = [id]   # 하나만 들어오면 요리 갯수 만큼 곱해주는 함수 위에 있음.
    item_id = recipe_ids            # 카테고리에 속한 요리 갯수 만큼 중복되지 않게 들어와야 함.
    recommends = predictions(user_id, item_id, model_path, Top_K=top_n)

    print('recommends:', recommends, flush=True)

    return recommends


# 추천 리스트
@recipe.post('/recommend/<page>')
def fetch_recommend(page):
    body = request.json or {}
    combination_id = 'combinationId' in body and body['combinationId'] or None

    limit = 50
    offset = (int(page) - 1) * limit

    recommends = get_recommend_ids(combination_id, top_n=50)

    # TODO: 나중에 추천모델 사용하도록 변경하기
    recipes = db.execute('fetchRecipeList.sql', {
        'ids': recommends,
        'limit': limit,
        'offset': offset,
    })

    return jsonify(recipes)


# 검색 (검색 리스트 + 추천 리스트)
@recipe.post('/<page>')
def fetch_list(page):
    body = request.json or {}
    ingredients = body['ingredients'] or None
    categories = body['categories'] or None
    combination_id = 'combinationId' in body and body['combinationId'] or None

    limit = 20
    offset = (int(page) - 1) * limit

    recommends = get_recommend_ids(combination_id, top_n=10)

    recipes = db.execute('searchRecipeList.sql', {
        'categories': categories,
        'ingredients': ingredients,
        'ids': recommends,
        'limit': limit,
        'offset': offset,
    })

    return jsonify(recipes)


@recipe.get('/favor')
def fetch_favor():
    favors = db.execute('fetchFavor.sql')
    return jsonify(favors)


@recipe.get('/combination')
def fetch_combination_id():
    favors = request.args.get('favors')
    favors = favors and favors.split(',')

    combination_id = db.execute('fetchCombinationId.sql', {
        'combination': favors
    })
    
    return jsonify(combination_id)


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
