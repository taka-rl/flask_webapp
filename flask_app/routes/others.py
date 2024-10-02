from flask import Blueprint, redirect, session, make_response, request

others_bp = Blueprint('others', __name__)


@others_bp.route('/switch_language/<lang>')
def switch_language(lang):
    session['lang'] = lang  # Store in session
    response = make_response(redirect(request.referrer))
    response.set_cookie('lang', lang, max_age=30*24*60*60)  # Store in cookie (30 days)
    return response
