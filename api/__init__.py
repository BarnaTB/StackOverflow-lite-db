from flask import Flask
from api.routes import mod
from api import routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(__name__)

# app.config.from_object('config.')
app.config['JWT_SECRET_KEY'] = 'my-kisumuluzo'
app.register_blueprint(routes.mod, url_prefix='/api/v1')
app.register_blueprint(routes.mod, url_prefix='/api/v1/auth')
app.register_blueprint(routes.mod, url_prefix='/api/v1/questions')

JWTManager(app)
Swagger(app)
