from flask import Blueprint
from flask_restful import Api
from api.resources.category import CategoryList, CategoryListByProduct, CategorySingle

CATEGORY_BLUEPRINT = Blueprint('categories', __name__)
Api(CATEGORY_BLUEPRINT).add_resource(CategoryList, '/api/categories/')
Api(CATEGORY_BLUEPRINT).add_resource(CategorySingle, '/api/categories/<cat>/')
Api(CATEGORY_BLUEPRINT).add_resource(CategoryListByProduct, '/api/categories/via-product/<prod>/')
