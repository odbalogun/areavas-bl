from flask_restful import Resource
from flasgger import swag_from
from api.repositories.product import ProductRepository
from api.repositories.subscriber import SubRepository
from api.models import Subscriber
from api.utils.extensions import ma
from api.utils.responses import response_success, response_error
from api.utils.error_codes import ERROR_RESOURCE_DOES_NOT_EXIST


class SubSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'msisdn', 'product_id', 'category_id', 'initial_sub_date', 'status', 'subscription_mode',
                  'last_renewed_date', 'expiry_date')
        model = Subscriber


class SubSingle(Resource):
    @staticmethod
    @swag_from('../docs/subscriber/GET.yml')
    def get(msisdn, prod):
        schema = SubSchema()
        product = ProductRepository.get(prod)
        if not product:
            return response_error(ERROR_RESOURCE_DOES_NOT_EXIST, "Product does not exist", status=404)
        sub = schema.dump(SubRepository.get(msisdn, product.id))
        if sub:
            return response_success(sub)
        return {}
