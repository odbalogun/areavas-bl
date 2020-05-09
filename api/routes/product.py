from flask import Blueprint
from flask_restful import Api
from api.resources.product import ProductList, ProductSingle

PRODUCT_BLUEPRINT = Blueprint('products', __name__)
Api(PRODUCT_BLUEPRINT).add_resource(ProductList, '/api/products/')
Api(PRODUCT_BLUEPRINT).add_resource(ProductSingle, '/api/products/<prod>/')
