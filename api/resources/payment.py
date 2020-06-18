from api.utils.extensions import ma
from api.utils.responses import response_success, response_error
from flask_restful import Resource


class PaymentSingle(Resource):
    @staticmethod
    def post():
        return response_success({'message': "Successfully processed"}, 201)
