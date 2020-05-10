from flask import Blueprint
from flask_restful import Api
from api.resources.subscriber import SubSingle

SUB_BLUEPRINT = Blueprint('subscribers', __name__)
Api(SUB_BLUEPRINT).add_resource(SubSingle, '/api/subscribers/<prod>/<msisdn>')
