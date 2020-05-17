import requests
from requests import Response
from app import app


class PaystackPay(object):
    """
     Paystack functions
    """
    def __init__(self):
        self.authorization_url = 'https://api.paystack.co/transaction/initialize'
        self.trans_verification_url = 'https://api.paystack.co/transaction/verify/{}'
        self.bvn_verification_url = 'https://api.paystack.co/bank/resolve_bvn/{}'

    def fetch_authorization_url(self, email, amount):
        payload = {
            'email': email,
            'amount': amount,
        }
        response: Response = requests.post(self.authorization_url, json=payload,
                                           headers={'Authorization': f'Bearer {app.config["PAYSTACK_KEY"]}'})
        return response

    def verify_reference_transaction(self, reference):
        response: Response = requests.get(self.trans_verification_url.format(reference),
                                          headers={'Authorization': f'Bearer {app.config["PAYSTACK_KEY"]}'})

        return response
