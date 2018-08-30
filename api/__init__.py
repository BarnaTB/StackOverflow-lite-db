from flask import Flask
from api.routes import mod
from api import routes
from flask_jwt_extended import JWTManager
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'my-kisumuluzo'
    app.config.from_object(app_config[config_name])
    app.register_blueprint(routes.mod, url_prefix='/api/v1')
    app.register_blueprint(routes.mod, url_prefix='/api/v1/auth')
    app.register_blueprint(routes.mod, url_prefix='/api/v1/questions')

    JWTManager(app)

    return app
