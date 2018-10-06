from flask import Flask
from api.routes import mod
from api import routes
from flask_jwt_extended import JWTManager
from flasgger import Swagger


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'my-kisumuluzo'
app.register_blueprint(routes.mod, url_prefix='/api/v1')

JWTManager(app)
Swagger(app)
