from flask import render_template, session, Blueprint, request, redirect, url_for
from models.users import get_all_info, get_user_id

bp = Blueprint('home', __name__)

@bp.route('/home', methods=['POST', 'GET'])
def home():
    comments = None
    start = False
    if request.method == 'POST':
        action = request.form.get('start')
        if action == 'start':
            start = True
        if action == 'save':
            name = request.form.get('username')
            info = None
            profile_picture = None

        comment_text = request.form.get('comment')
        author_id = get_user_id(session['email'])
    user_id, role, events, joined_events=get_all_info(session['email'])
    return render_template('home.html', username=session['username'], email=session['email'],
                           events=events, joined_events=joined_events, role=role[0], commets=comments, start=start)
