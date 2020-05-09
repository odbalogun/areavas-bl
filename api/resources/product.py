from flask_restful import Resource
from flasgger import swag_from
from api.repositories.product import ProductRepository
from api.models.product import Product
from api.utils.responses import response_success, response_error
from api.utils.error_codes import ERROR_RESOURCE_DOES_NOT_EXIST
from api.utils.pagination import paginate
from api.utils.extensions import ma
from .category import CategorySchema


class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'name', 'slug', 'categories')
        model = Product

    categories = ma.List(ma.Nested(CategorySchema))


class ProductSingle(Resource):
    @staticmethod
    @swag_from('../docs/product/GET.yml')
    def get(prod):
        schema = ProductSchema()
        product = ProductRepository.get(prod)
        if not product:
            return response_error(ERROR_RESOURCE_DOES_NOT_EXIST, "Product does not exist", status=404)
        return response_success(schema.dump(product))


class ProductList(Resource):
    method_decorators = []

    @staticmethod
    @swag_from('../docs/product-list/GET.yml')
    def get():
        schema = ProductSchema(many=True)
        return response_success(paginate(ProductRepository.get_all(), schema))