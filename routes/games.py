from flask import render_template, session, Blueprint, request

from models.users import start_game, get_user_id

games_bp = Blueprint('games', __name__)

@games_bp.route('/games-events', methods=['POST', 'GET'])
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
                if validate_name(name_event):
                    if validate_date(start_date, end_date):
                        user=get_user_id()

                        if not user:
                            conn.close()
                            return redirect(url_for('login'))
                        else:
                            user_id = user[0]

                        cursor.execute(
                            "INSERT INTO events (name_events, info, start_date, end_date, user_id) VALUES (?, ?, ?, ?, ?)",
                            (name_event, info, start_date, end_date, user_id))
                        #events_number+=1
                        conn.commit()
                        conn.close()
                    else:
                        error = 'Wrong data'
                else:
                    error = 'Event already created'

            else:
                error = 'Check all lines'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_events, start_date FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template('games_events.html', start=start, error=error, events=events)
