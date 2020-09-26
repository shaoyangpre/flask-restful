from flask import Flask
from apps.home import home as home_blueprint


def register_blueprints(app):
    from apps.api.v1 import create_v1_blueprint
    app.register_blueprint(create_v1_blueprint(), url_prefix='/v1')
    app.register_blueprint(home_blueprint, url_prefix = '/home')

def register_plugin(app):
    from apps.model import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

def creat_app():
    app = Flask(__name__)

    app.config.from_object('apps.config.setting')
    app.config.from_object('apps.config.secure')

    register_blueprints(app)
    register_plugin(app)

    return app

