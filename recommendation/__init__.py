from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from .config import Config
import os



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    
    login_manager.login_view = 'users.login'
    login_manager.login_message_category = 'info'
    
    from recommendation.user.routes import users
    from recommendation.admin.routes import admin
    
    app.register_blueprint(users)
    app.register_blueprint(admin)
    
    return app

