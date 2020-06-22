from flask import Blueprint
from flask_restful import Api
from api.resources.category import CategoryList, CategorySingle

CATEGORY_BLUEPRINT = Blueprint('categories', __name__)
Api(CATEGORY_BLUEPRINT).add_resource(CategoryList, '/api/categories/')
Api(CATEGORY_BLUEPRINT).add_resource(CategorySingle, '/api/categories/<cat>/')
