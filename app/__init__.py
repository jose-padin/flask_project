from flask import Flask
from flask_bootstrap import Bootstrap

from .auth import auth
from .config import Config

def create_app():

    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)
    
    app.register_blueprint(auth)

    return app