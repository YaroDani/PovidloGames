from flask import render_template, session, Blueprint, request, redirect, url_for
from models.events import get_info_a_event, create_game, get_all_events, get_user_name
from models.users import start_game, get_user_id
from utils.util import validate_name, validate_date, get_db_connection

bp = Blueprint('games', __name__)

@bp.route('/games-events', methods=['POST', 'GET'])
def games():
    start = None
    error = None

    if request.method == 'POST':
        action = request.form.get('start') # 3 value: start, close, create

        if action == 'start':
            user_info,events_count=start_game(session['email'])
            if events_count>= 3 and user_info[1]=="user":
                error = 'You have used all free events creations'
                start = False
            else:
                start = True
        if action == 'close':
            start = False

        if action == 'create':
            name_event = request.form.get('name_event')
            info = request.form.get('info')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            if name_event and info and start_date and end_date:
                name_event = get_user_name(name_event)
                if validate_name(name_event):
                    if validate_date(start_date, end_date):
                        user=get_user_id(session['email'])
                        if not user:
                            return redirect(url_for('login'))
                        else:
                            user_id = user[0]
                            create_game(name_event, info, start_date, end_date, user_id)
                    else:
                        error = 'Wrong data'
                else:
                    error = 'Event already created'

            else:
                error = 'Check all lines'

    events = get_all_events()
    return render_template('games_events.html', start=start, error=error, events=events)

@bp.route('/event-<event_name>', methods=['POST', 'GET'])
def event_page(event_name):
    events = get_info_a_event(event_name)
    conn = get_db_connection()
    cursor = conn.cursor()
    username_author = cursor.execute("SELECT username FROM users WHERE id = ?", (events[0][4], ))
    username_author = username_author.fetchone()

    #cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))

    if request.method == 'POST':

        cursor.execute("Select id FROM users WHERE email=?", (session["email"],))
        id=cursor.fetchone()
        cursor.execute("SELECT name_events FROM joined_events WHERE user_id=? AND name_events=?", (id[0],events[0][0]))
        info = cursor.fetchall()
        if not info:
            cursor.execute("INSERT INTO joined_events (name_events, user_id) VALUES (?,?)", (events[0][0],id[0]))
            conn.commit()
            conn.close()

    return render_template('eventpage.html',name_author=username_author[0], name_event=event_name, info_event=events[0][1], start_date=events[0][2], end_date=events[0][3])
