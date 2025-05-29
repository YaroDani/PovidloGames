from flask import render_template, Blueprint
from models.users import get_all_info, get_user_id
from utils.util import get_db_connection

bp = Blueprint('profiles', __name__)


@bp.route('/profile-<username>', methods=['POST', 'GET'])
def profile_page(username):
    print(username)
    comments = None
    conn=get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE username=?", (username,))
    email = cursor.fetchone()
    user_id, role, events, joined_events = get_all_info(email[0])
    joined_events = [row[0] for row in joined_events]
    cursor.execute("SELECT text FROM comments WHERE user_id=?", (user_id[0],))
    comments = cursor.fetchone()
    return render_template('profile.html', username=username,
                           events=events,
                           joined_events=joined_events,
                           role=role[0],
                           comments=comments)
