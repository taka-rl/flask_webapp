from flask import Blueprint, render_template, request
from flask_app.utils import with_translations, admin_only, get_weather_info, get_currency_info

useful_info_bp = Blueprint('useful_info', __name__)


@useful_info_bp.route("/useful_info")
@with_translations
def useful_info():
    return render_template("useful_info.html")


@useful_info_bp.route('/weather', methods=["POST", "GET"])
@admin_only
@with_translations
def show_weather():
    if request.method == "POST":
        location = request.form["loc"]
        weather_data = get_weather_info(location)

    return render_template('weather.html', loc=location, weather_data=weather_data)


@useful_info_bp.route('/currency', methods=["POST"])
@admin_only
@with_translations
def get_currency():
    currency_data = get_currency_info()
    return currency_data
