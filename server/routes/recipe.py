from flask import Blueprint, request
from models.recommenders.models.prediction import predictions, get_data, theme_dic

recipe = Blueprint('recipe', __name__, url_prefix='/recipe')


@recipe.post('/<type>/<page>')
def fetch_list(type, page):
    body = request.form

    ingredients = body.get('ingredients')
    categories = body.get('categories')

    # print('*' * 30, flush=True)
    # print(sys.path, flush=True)
    # recommends_top10 = predictions(597, ['한식', '분식', '다이어트'])
    # print(recommends_top10, flush=True)

    return f'fetch_list {type} {page} {ingredients} {categories}'


@recipe.get('/<id>')
def fetch_detail(id):
    return f'fetch_detail {id}'


@recipe.post('/<id>')
def rating(id):
    body = request.form

    rating = body.get('rating')

    return f'rating {id} {rating}'
