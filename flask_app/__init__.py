from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask import Flask
from flask_login import LoginManager


from flask_app.models import User
from flask_app.models import db
from flask_app.config import config

login_manager = LoginManager()


def create_app(config_name):
    # Initialize extensions
    # db = SQLAlchemy()  db is defined in models.py
    ckeditor = CKEditor()
    bootstrap = Bootstrap5()

    # Create Flask app instance
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Load the appropriate config for the environment
    app.config.from_object(config[config_name])

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
    from flask_app.routes.errors import errors_bp
    from flask_app.routes.admin import admin_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(collection_bp)
    app.register_blueprint(useful_info_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(others_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(admin_bp)

    # Create the database table
    with app.app_context():
        db.create_all()

    return app
