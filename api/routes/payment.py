from flask import Blueprint
from flask_restful import Api
from api.resources.payment import PaymentSingle

PAYMENT_BLUEPRINT = Blueprint('payments', __name__)
Api(PAYMENT_BLUEPRINT).add_resource(PaymentSingle, '/api/payments/')