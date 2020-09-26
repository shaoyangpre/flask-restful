"""
 Created by 七月 on 2018/5/10.
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp
from wtforms import ValidationError

from apps.libs.enums import ClientTypeEnum
from apps.model.user import User
from apps.validator.base import BaseForm as Form

__author__ = '七月'


class ClientForm(Form):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        # self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    name = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
