from flask import Blueprint, render_template_string, request, redirect
from api.models import Transaction, Category
from api.utils.payments import PaystackPay
from api.utils.formatters import msisdn_formatter


blueprint = Blueprint("pages", __name__)


@blueprint.route('/page')
def page():
    return render_template_string("This works")


@blueprint.route('/webpay', methods=['POST'])
def webpay():
    # check that form has necessary fields
    form = request.form

    if not form.get('msisdn') or not form.get('price') or not form.get('mode') or not form.get('txn_type'):
        return render_template_string("Error: Mandatory field not provided")

    # create Transaction item
    msisdn = msisdn_formatter(form.get('msisdn'))
    tran = Transaction(msisdn=msisdn, price=form.get('price'), mode=form.get('mode'), txn_type=form.get('txn_type'),
                       category_id=form.get('category_id'), user_id=form.get('user_id'), items=form.get('items'))
    tran.save()

    # call Paystack api to create transaction
    paystack = PaystackPay()
    if form.get('category_id'):
        cat = Category.query.get(form.get('category_id'))
        response = paystack.fetch_authorization_url(email=tran.identity_email, amount=form.get('price'),
                                                    plan=cat.plan_code)
    else:
        response = paystack.fetch_authorization_url(email=tran.identity_email, amount=form.get('price'))

    # save transaction information
    data = response.json()
    if data.get('status'):
        tran.txn_reference = data.get('data').get('reference')
        tran.save()

        # redirect to paystack payment page
        redirect(data.get('data').get('authorization_url'))
    return render_template_string("Error: Something went wrong. Please contact an administrator")


@blueprint.route('/process-transaction', methods=['GET', 'POST'])
def process_txn():
    reference = request.args.get('reference')

    if not reference:
        return render_template_string("Error: No reference found")

    # fetch transaction
    tran = Transaction.query.filter_by(txn_reference=reference).first()

    if tran:
        # check if value has already been given
        if tran.status != 0:
            return render_template_string("Error: This transaction is no longer valid")
        # verify transaction
        paystack = PaystackPay()
        response = paystack.verify_reference_transaction(reference=reference)

        if response.status_code == 200:
            # update transaction
            tran.status = 2
            tran.save()

            # todo add to billing logs
            # todo add to subscription

            # todo find out if there's any api to call on mobile app
            return render_template_string("Success: Transaction has been completed")
        else:
            return render_template_string("Error: The transaction could not be completed")
    return render_template_string("Error: No transaction found")


@blueprint.route('/process-transaction-hook', methods=['GET', 'POST'])
def process_txn_hook():
    # todo this function should return JSON
    reference = request.args.get('reference')

    if not reference:
        return render_template_string("Error: No reference found")

    # fetch transaction
    tran = Transaction.query.filter_by(txn_reference=reference).first()

    if tran:
        # check if value has already been given
        if tran.status != 0:
            return render_template_string("Error: This transaction is no longer valid")
        # verify transaction
        paystack = PaystackPay()
        response = paystack.verify_reference_transaction(reference=reference)

        if response.status_code == 200:
            # update transaction
            tran.status = 2
            tran.save()

            # todo add to billing logs
            # todo add to subscription
            # todo find out if there's any api to call on mobile app
            return render_template_string("Success: Transaction has been completed")
        else:
            return render_template_string("Error: The transaction could not be completed")
    return render_template_string("Error: No transaction found")