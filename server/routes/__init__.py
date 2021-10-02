from flask import Blueprint

from .recipe import recipe
from .ingredient import ingredient
from .category import category

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(recipe)
api.register_blueprint(ingredient)
api.register_blueprint(category)
