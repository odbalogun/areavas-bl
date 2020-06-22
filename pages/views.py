from flask import Blueprint, render_template_string, request, redirect
from api.models import Transaction
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

    if not form.get('msisdn') or not form.get('amount') or not form.get('payment_mode') or not form.get('payment_type'):
        return render_template_string("Error: Mandatory field not provided")

    # check that payment_type is either subscription or purchase
    if form.get('payment_type') not in PaymentTypeEnum:
        return render_template_string("Error: Invalid payment type")

    # check that if it is purchase it contains line items
    if form.get('payment_type') == PaymentTypeEnum.PURCHASE and not form.get('items'):
        return render_template_string("Error: No line items provided")

    # check that if it is subscription it does not contain line items
    if form.get('payment_type') == PaymentTypeEnum.SUBSCRIPTION and form.get('items'):
        return render_template_string("Error: Cannot provide line items for subscription")

    # check that subscription have a category id & product id
    if form.get('payment_type') == PaymentTypeEnum.SUBSCRIPTION and (form.get('category_id') or form.get('product_id')):
        return render_template_string("Error: No category/product provided")

    # create Transaction item
    msisdn = msisdn_formatter(form.get('msisdn'))
    tran = Transaction(msisdn=msisdn, amount=form.get('amount'), payment_mode=form.get('payment_mode'),
                       payment_type=form.get('payment_type'), category_id=form.get('category_id'),
                       product_id=form.get('product_id'), subscriber_id=form.get('subscriber_id'))

    for item in form.get('items'):
        tran.items.append(TransactionItem(item=item))

    tran.save()

    # call Paystack api to create transaction
    paystack = PaystackPay()
    if form.get('category_id'):
        cat = ProductCategory.query.get(form.get('category_id'))
        response = paystack.fetch_authorization_url(email=tran.identity_email, amount=form.get('amount'),
                                                    plan=cat.plan_code)
    else:
        response = paystack.fetch_authorization_url(email=tran.identity_email, amount=form.get('amount'))

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
        if tran.status == StatusEnum.Paid:
            return render_template_string("Success: Transaction has been completed")
        # verify transaction
        paystack = PaystackPay()
        response = paystack.verify_reference_transaction(reference=reference)

        if response.status_code == 200:
            # update transaction
            tran.status = StatusEnum.Paid
            tran.save()
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
        if tran.status == StatusEnum.Paid:
            return render_template_string("Success: Transaction has been completed")
        # verify transaction
        paystack = PaystackPay()
        response = paystack.verify_reference_transaction(reference=reference)

        if response.status_code == 200:
            # update transaction
            tran.status = StatusEnum.Paid
            tran.save()
            # todo find out if there's any api to call on mobile app
            return render_template_string("Success: Transaction has been completed")
        else:
            return render_template_string("Error: The transaction could not be completed")
    return render_template_string("Error: No transaction found")