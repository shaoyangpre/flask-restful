from flask import Blueprint
from apps.api.v1 import book,user,token

def create_v1_blueprint():
    v1 = Blueprint('v1', __name__)

    book.api.register(v1)
    user.api.register(v1)
    token.api.register(v1)

    return v1



