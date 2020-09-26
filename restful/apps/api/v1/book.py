from flask import request,g,session,jsonify,render_template

from apps.libs.redprint import Redprint

api = Redprint('book')


@api.route('/detail', methods = ['GET'])
def detail():
    return render_template("ajax.html")

@api.route('/ajax', methods = ["POST"])
def ajax():
    da = request
    a = 1
    pass
