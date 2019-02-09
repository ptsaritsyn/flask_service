from app import app
from flask import Blueprint
from flask import render_template
from flask import request, redirect
from flask import Markup
from .service import Service


service_app = Blueprint('service', __name__, template_folder='templates')


@service_app.route('/')
def index():
    return render_template('service/index.html')


@service_app.route('/confirm', methods=['POST'])
def main_handler():
    try:
        amount = Markup(request.form.get('amount', '')).striptags()
        currency = Markup(request.form.get('currency', '')).striptags()
        description = Markup(request.form.get('description')).striptags()

        if amount and currency and amount.isdigit():
            service = Service(amount, currency, description)
            sign = service.generate_sign(amount=service.amount,
                                         currency=service.currency,
                                         shop_id=service.shop_id,
                                         shop_order_id=service.shop_order_id)

            if currency == '978':
                service.write_log(file_name='pay.log')
                return render_template('service/pay_form.html',
                                       amount=service.amount,
                                       currency=service.currency,
                                       description=service.description,
                                       sign=sign,
                                       shop_order_id=service.shop_order_id,
                                       currency_name='EUR')

            if currency == '840':
                service.write_log(file_name='bill.log')
                service.generate_sign(shop_amount=service.amount,
                                      shop_currency=service.currency,
                                      shop_id=service.shop_id,
                                      shop_order_id=service.shop_order_id,
                                      payer_currency=service.currency)
                service.url = 'https://core.piastrix.com/bill/create'
                service.method = 'bill'
                method_data = service.get_method_data()
                data = service.send_method_data(method_data)
                return redirect(data["data"]["url"])

            if currency == '643':
                service.write_log(file_name='invoice.log')
                service.generate_sign(amount=service.amount,
                                      currency=service.currency,
                                      shop_id=service.shop_id,
                                      shop_order_id=service.shop_order_id,
                                      payway=service.payway)
                service.url = 'https://core.piastrix.com/invoice/create'
                service.method = 'invoice'
                method_data = service.get_method_data()
                data = service.send_method_data(method_data)
                return render_template('service/invoice_form.html', data=data['data'], currency_name='RUB',
                                       amount=service.amount)
        else:
            return render_template('service/index.html', empty=True)
    except Exception as e:
        app.logger.error('Exception: %s', (e))
        return render_template('500.html'), 500
