from flask import Blueprint, render_template
from flask_app.utils import with_translations


errors_bp = Blueprint('errors', __name__)


# 404 Not Found
@errors_bp.app_errorhandler(404)
@with_translations
def not_found(error):
    return render_template('404.html'), 404


# 403 Forbidden
@errors_bp.app_errorhandler(403)
@with_translations
def forbidden(error):
    return render_template('403.html'), 403


# 500 Internal Server Error
@errors_bp.app_errorhandler(500)
@with_translations
def server_error(error):
    return render_template('500.html'), 500
