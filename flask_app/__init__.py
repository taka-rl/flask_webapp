from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask import Flask
from flask_login import LoginManager
import os
from dotenv import load_dotenv

from flask_app.models import User
from flask_app.models import db

login_manager = LoginManager()


def create_app():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize extensions
    # db = SQLAlchemy()  db is defined in models.py
    ckeditor = CKEditor()
    bootstrap = Bootstrap5()

    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Initialize app with extentions
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)

    # Import blueprints (routes)
    from flask_app.routes.auth import auth_bp
    from flask_app.routes.blog import blog_bp
    from flask_app.routes.collection import collection_bp
    from flask_app.routes.useful_info import useful_info_bp
    from flask_app.routes.about import about_bp
    from flask_app.routes.contact import contact_bp
    from flask_app.routes.others import others_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(useful_info_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(others_bp)

    return app


# User loader callback function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Query the user by ID
