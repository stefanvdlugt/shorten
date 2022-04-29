from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    prefix = app.config['BASE_URL']

    from .main import main
    app.register_blueprint(main, url_prefix=prefix)

    from .auth import auth
    app.register_blueprint(auth, url_prefix=prefix+'/auth')

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)

    return app

from . import models
