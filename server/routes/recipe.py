from flask import Blueprint, request

recipe = Blueprint('recipe', __name__, url_prefix='/recipe')


@recipe.post('/<type>/<page>')
def fetch_list(type, page):
    body = request.form

    ingredients = body.get('ingredients')
    categories = body.get('categories')
    gender = body.get('gender')
    theme = body.get('theme')

    return f'fetch_list {type} {page} {ingredients} {categories} {gender} {theme}'


@recipe.get('/<id>')
def fetch_detail(id):
    return f'fetch_detail {id}'


@recipe.post('/<id>')
def rating(id):
    body = request.form

    rating = body.get('rating')

    return f'rating {id} {rating}'
