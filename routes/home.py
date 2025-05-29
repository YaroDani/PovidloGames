from flask import render_template, session, Blueprint, request, redirect, url_for, send_file
from utils.util import get_db_connection
from models.users import get_all_info, get_user_id
import io
import re

bp = Blueprint('home', __name__)

def clean_filename(filename):
    """Проста заміна небажаних символів у назві файлу (альтернатива secure_filename)."""
    return re.sub(r'[^A-Za-z0-9_.-]', '_', filename)

@bp.route('/home', methods=['POST', 'GET'])
def home():
    comments = None
    start = False

    if request.method == 'POST':
        action = request.form.get('start') or request.form.get('save')
        if action == 'start':
            start = True
        elif action == 'save':
            name = request.form.get('username')
            if name:
                session['username'] = name
            file = request.files.get('file')
            user_id = get_user_id(session['email'])

            conn = get_db_connection()
            if file and file.filename:
                filename = clean_filename(file.filename)
                data = file.read()
                conn.execute("UPDATE users SET username = ?, pfp = ? WHERE id = ?", (name, data, user_id))
            else:
                conn.execute("UPDATE users SET username = ? WHERE id = ?", (name, user_id))
            conn.commit()
            conn.close()
            session['username'] = name
    print(session['email'])
    user_id, role, events, joined_events = get_all_info(session['email'])
    joined_events = [row[0] for row in joined_events]
    return render_template('home.html',
                           username=session['username'],
                           email=session['email'],
                           events=events,
                           joined_events=joined_events,
                           role=role[0],
                           comments=comments,
                           start=start)


@bp.route('/pfp/email/<email>')
def pfp_by_email(email):
    conn = get_db_connection()
    row = conn.execute("SELECT pfp FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    if row and row[0]:
        return send_file(io.BytesIO(row[0]), mimetype='image/png')
    return redirect("https://via.placeholder.com/150")
