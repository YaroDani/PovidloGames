from flask import render_template, session, Blueprint, request, redirect, url_for
from models.users import get_all_info

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['POST', 'GET'])
def home():
    user_id, role, events, joined_events=get_all_info(session['email'])
    return render_template('home.html', username=session['username'], email=session['email'],
                           events=events, joined_events=joined_events, role=role[0])