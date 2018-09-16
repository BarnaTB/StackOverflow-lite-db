from flask import Flask
from api.routes import mod
from api import routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger


# def create_app():
app = Flask(__name__)

# app.config.from_object(DevelopmentConfig)
app.config['JWT_SECRET_KEY'] = 'my-kisumuluzo'
app.register_blueprint(routes.mod, url_prefix='/api/v1')
app.register_blueprint(routes.mod, url_prefix='/api/v1/auth')
app.register_blueprint(routes.mod, url_prefix='/api/v1/questions')

JWTManager(app)
Swagger(app)

# return app
