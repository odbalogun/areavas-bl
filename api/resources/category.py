from flask_restful import Resource
from flasgger import swag_from
from api.repositories.category import CategoryRepository
from api.models import Category
from api.utils.responses import response_success, response_error
from api.utils.error_codes import ERROR_RESOURCE_DOES_NOT_EXIST
from api.utils.pagination import paginate
from api.utils.extensions import ma


class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'product_id', 'name', 'slug', 'price', 'validity')
        model = Category


class CategorySingle(Resource):
    @staticmethod
    @swag_from('../docs/category/GET.yml')
    def get(cat):
        schema = CategorySchema()
        category = CategoryRepository.get(cat)
        if not category:
            return response_error(ERROR_RESOURCE_DOES_NOT_EXIST, "Category does not exist", status=404)
        return response_success(schema.dump(category))


class CategoryList(Resource):
    @staticmethod
    @swag_from('../docs/category-list/GET.yml')
    def get():
        schema = CategorySchema(many=True)
        return response_success(paginate(CategoryRepository.get_all(), schema))