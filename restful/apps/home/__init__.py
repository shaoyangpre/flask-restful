from flask import Blueprint,request
from flask_login import login_user

home = Blueprint('home', __name__)

@home.route('/home', methods = ['GET'])
def add():
    q = request
    return 'sss'