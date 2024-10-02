from flask import Blueprint, render_template, request
from flask_app.utils import with_translations, send_email

contact_bp = Blueprint('contact', __name__)


@contact_bp.route("/contact")
@with_translations
def contact():
    return render_template("contact.html")


@contact_bp.route("/contact", methods=["POST", "GET"])
@with_translations
def receive_data():
    if request.method == "POST":
        subject = request.form["subject"]
        name = request.form["name"]
        to_email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        # automatically send to the questioner
        send_email(to_email=to_email, name=name, phone=phone, subject=subject, message=message)

        return render_template('contact.html', msg_sent=True)
    else:
        return render_template('contact.html')
    