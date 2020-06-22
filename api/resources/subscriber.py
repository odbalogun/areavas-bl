from flask_restful import Resource
from flasgger import swag_from
from api.repositories.subscriber import SubRepository
from api.models import Subscription
from api.utils.extensions import ma
from api.utils.responses import response_success


class SubSchema(ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'msisdn', 'product_id', 'category_id', 'initial_sub_date', 'status', 'subscription_mode',
                  'last_renewed_date', 'expiry_date')
        model = Subscription


class SubSingle(Resource):
    @staticmethod
    @swag_from('../docs/subscriber/GET.yml')
    def get(msisdn):
        schema = SubSchema()
        sub = schema.dump(SubRepository.get(msisdn))
        if sub:
            return response_success(sub)
        return {}
