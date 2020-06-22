from api.models import Subscription
from api.utils.formatters import msisdn_formatter


class SubRepository:

    @staticmethod
    def get(msisdn):
        msisdn = msisdn_formatter(msisdn)
        return Subscription.query.filter_by(msisdn=msisdn).first()
