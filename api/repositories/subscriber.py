from api.models import Subscriber
from api.utils.formatters import msisdn_formatter


class SubRepository:

    @staticmethod
    def get(msisdn, prod):
        msisdn = msisdn_formatter(msisdn)
        return Subscriber.query.filter_by(product_id=prod, msisdn=msisdn).first()
