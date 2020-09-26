from flask import request, g, session, render_template, jsonify, current_app, url_for

from apps.libs.Alipay import OrderAlipay
from apps.libs.error_code import Success
from apps.libs.redprint import Redprint
from apps.libs.token_auth import auth
from apps.model import db
from apps.libs.enums import ClientTypeEnum
from apps.model.user import User
from apps.validator.forms import ClientForm, UserEmailForm
from flask_login import login_required


api = Redprint('user')


@api.route('/register', methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[ClientTypeEnum(form.type.data)]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.name.data,
                           form.account.data,
                           form.secret.data)

@api.route('/get_user', methods = ['POST'])
# @auth.login_required
def get_user():
    a = User.query.filter_by(email='12222').first()
    pass


@api.route('/get_url', methods = ['POST'])
def get_url():
    type = 'pc'
    out_trade_no = '20182332323778934482'
    total_amount = 30002.00
    subject = '小胖子美食'
    return_url = 'http://127.0.0.1:5000/v1/user/success'

    Myalipay = OrderAlipay(current_app)
    url_data = Myalipay.get_pay_url(type, out_trade_no, total_amount, subject, return_url)

    return url_data


@api.route('/get_tk', methods=['POST'])
def tuikuang():
    Myalipay = OrderAlipay(current_app)
    restult = Myalipay.refund(30002.00,'20182332323778934482','2019122622001468121000033631')
    return restult


@api.route('/success', methods=['GET'])
def success():
    return render_template('success.html')


@api.route('/url', methods=['GET'])
def url():
    return render_template('url.html')