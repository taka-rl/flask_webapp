from flask import Blueprint, render_template
from flask_app.utils import with_translations

about_bp = Blueprint('about', __name__)


@about_bp.route("/about")
@with_translations
def about():
    return render_template("about.html")
