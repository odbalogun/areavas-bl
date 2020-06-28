from flask import Blueprint
from flask_restful import Api
from api.resources.transactions import SubscribeAction, UnsubscribeAction, PurchaseAction

ACTION_BLUEPRINT = Blueprint('actions', __name__)
Api(ACTION_BLUEPRINT).add_resource(SubscribeAction, '/api/actions/subscribe')
Api(ACTION_BLUEPRINT).add_resource(UnsubscribeAction, '/api/actions/unsubscribe/<identifier>')
Api(ACTION_BLUEPRINT).add_resource(PurchaseAction, '/api/actions/purchase')
