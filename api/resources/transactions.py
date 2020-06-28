from flask_restful import Resource, reqparse
from flasgger import swag_from
from api.models import Transaction, User, Subscription, Category, BillingLog, UnsubscriptionLog
from api.utils.extensions import ma
from api.utils.responses import response_success, response_error
from api.utils.formatters import msisdn_formatter
from flask import jsonify
from marshmallow import INCLUDE, post_load
import datetime


class TransactionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Transaction
        unknown = INCLUDE

    @post_load
    def make_user(self, data, **kwargs):
        return Transaction(**data)


class SubscribeAction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price', type=int, required=True, help='Price not provided', location='json')
        self.parser.add_argument('mode', type=int, required=False, default=0, location='json')
        self.parser.add_argument('txn_type', type=int, required=False, default=0, location='json')
        self.parser.add_argument('msisdn', type=str, required=True, location='json')
        self.parser.add_argument('user_id', type=int, required=False, default=None, location='json')
        self.parser.add_argument('category_id', type=int, required=True, location='json')
        super(SubscribeAction, self).__init__()

    def post(self):
        # todo add actual subscription logic for mtn & paystack
        args = self.parser.parse_args()
        schema = TransactionSchema()
        errors = schema.validate(args)
        if errors:
            return response_error(message=errors, code=400)
        tran = schema.load(args)
        # check that category exists
        if not Category.query.get(tran.category_id):
            return response_error(404, "Specified category does not exist", 404)
        tran.status = 1
        tran.msisdn = msisdn_formatter(tran.msisdn)
        tran.save()

        # create actual subscription
        if tran.user_id:
            user = User.query.get(tran.user_id)
            if not user:
                tran.delete()
                return response_error(404, "Specified user does not exist", 404)
        else:
            user = User.create_or_get(msisdn=tran.msisdn)
        if user.subscription:
            user.subscription.mode = tran.mode
            user.subscription.category_id = tran.category_id
            user.subscription.date_updated = datetime.datetime.now()
            user.subscription.expiry_date = datetime.datetime.now() + datetime.timedelta(days=tran.category.validity)
        else:
            user.subscription = Subscription(mode=tran.mode, category_id=tran.category_id,
                                             expiry_date=datetime.datetime.now() + datetime.timedelta(
                                                 days=tran.category.validity))
        user.save()

        # add billing log
        bill = BillingLog(user_id=user.id, category_id=tran.category_id, validity=tran.category.validity,
                          price=tran.price, mode=tran.mode, txn_type=tran.txn_type)
        bill.save()
        return response_success(schema.dump(tran))


class UnsubscribeAction(Resource):
    @staticmethod
    def get(identifier):
        user = User.query.filter(User.id == identifier | User.msisdn == msisdn_formatter(identifier)).first()
        if not user:
            return response_error(404, "Requested user does not exist", 404)
        if not user.subscription:
            return response_error(400, "User is not subscribed", 400)

        if user.subscription.mode == 0:
            # todo add unsubscribe logic for paystack
            pass
        elif user.subscription.mode == 1:
            # todo add unsubscribe logic for mtn
            pass

        # add to unsubscribe log
        user.unsubscription_logs.append(UnsubscriptionLog(category_id=user.subscription.category_id,
                                                          mode=user.subscription.mode))
        # delete details
        user.subscription = None
        user.save()
        return response_success("User has been successfully unsubscribed")


class PurchaseAction(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('price', type=int, required=True, help='Price not provided', location='json')
        self.parser.add_argument('items', type=str, required=True, location='json')
        self.parser.add_argument('mode', type=int, required=False, default=0, location='json')
        self.parser.add_argument('txn_type', type=int, required=False, default=0, location='json')
        self.parser.add_argument('msisdn', type=str, required=True, location='json')
        self.parser.add_argument('user_id', type=int, required=False, default=None, location='json')
        self.parser.add_argument('category_id', type=int, required=True, location='json')
        super(PurchaseAction, self).__init__()

    @staticmethod
    def post():
        pass