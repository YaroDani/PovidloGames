from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn
    # cursor = conn.cursor()


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

'''
@app.route('/')
def main_page():
    show_button=None
    if session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE email=?", (session["email"],))
        role=cursor.fetchone()
        if role[0] == "admin":
            show_button=True
        else:
            show_button=False
    return render_template('main.html', show_button=show_button)
'''
'''
@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if request.method == "POST":
        if email and password and username:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT email FROM users WHERE email=?", (email,))
            user_email = cursor.fetchone()
            cursor.execute("SELECT username FROM users WHERE username=?", (username,))
            user_name = cursor.fetchone()
            print(user_email)
            if user_email:
                error = 'Email already exists'
                conn.close()
            elif user_name:
                error="username already exists"
                conn.close()
            else:
                cursor.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)",
                               (email, username, password, "user"))
                conn.commit()
                conn.close()

                session['username'] = username
                session['email'] = email
                return redirect(url_for('home'))

    return render_template('register.html', error=error)
'''
'''
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                if user[3] == password:

                    session['username'] = user[2]
                    session['email'] = user[1]
                    return redirect(url_for('home'))
                else:
                    error = 'Password error'
            else:
                error = 'Email error'

    return render_template('login.html', error=error)
'''
'''
@app.route('/home', methods=['POST', 'GET'])
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (session['email'],))
    user_id = cursor.fetchone()
    cursor.execute("SELECT role FROM users WHERE email=?", (session["email"],))
    role = cursor.fetchone()
    cursor.execute("SELECT name_events, start_date FROM events WHERE user_id=?", (user_id[0],))
    events = cursor.fetchall()
    # НАЗВИ ІВЕНТІВ ДО ЯКИХ МИ ПРИЄДНАЛИСЯ
    cursor.execute("SELECT name_events FROM joined_events WHERE user_id=? ", (user_id[0],))
    joined_events = cursor.fetchall()
    # отримати дату приєднаних ві
    conn.close()
    return render_template('home.html', username=session['username'], email=session['email'], events=events, joined_events=joined_events, role=role[0])
'''

'''
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))'''


'''
def validate_date(start_date, end_date):
    error = None
    data_s = list(map(int, start_date.split("-")))
    date_e = list(map(int, end_date.split("-")))
    if data_s[0] == date_e[0]:
        data_s[1] -= 1
        date_e[1] -= 1
        data_s[1] *= 30
        date_e[1] *= 30

        if data_s[0] + data_s[1] + data_s[2] < date_e[0] + date_e[1] + date_e[2]:
            # print("Все правильно")
            return True
        else:
            # print("Дата кінця раніша за початок")
            return error

    elif data_s[0] < date_e[0]:
        # print("Все правильно")
        return True
    else:
        # print("Дата кінця раніша за початок")
        return error


def validate_name(name_event):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM events WHERE name_events = ?', (name_event,))
    result = cursor.fetchone()
    if result:
        return False
    return True
'''
'''
@app.route('/games-events', methods=['POST', 'GET'])
def games():
    start = None
    error = None



    if request.method == 'POST':
        action = request.form.get('start') # 3 value: start, close, create

        if action == 'start':
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT id,role FROM users WHERE email = ?', (session['email'],))
            user_info = cursor.fetchone()
            cursor.execute("SELECT name_events FROM events WHERE user_id=?", (user_info[0],))
            events = cursor.fetchall()
            events_count=len(events)
            print(events_count)
            print(user_info)
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
            print(name_event, info, start_date, end_date)
            if name_event and info and start_date and end_date:
                if validate_name(name_event):
                    if validate_date(start_date, end_date):
                        conn = get_db_connection()
                        cursor = conn.cursor()

                        cursor.execute('SELECT id FROM users WHERE email=?', (session['email'],))
                        user = cursor.fetchone()

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

@app.route('/event-<event_name>', methods=['POST', 'GET'])
def event_page(event_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_events, info, start_date, end_date, user_id FROM events WHERE name_events = ?",
                   (event_name,))
    events = cursor.fetchall() # id_user [0][]

    username_author = cursor.execute("SELECT username FROM users WHERE id = ?", (events[0][4], ))
    username_author = username_author.fetchone()

    #cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)", (email, username, password))

    if request.method == 'POST':

        cursor.execute("Select id FROM users WHERE email=?", (session["email"],))
        id=cursor.fetchone()
        cursor.execute("SELECT name_events FROM joined_events WHERE user_id=? AND name_events=?", (id[0],events[0][0]))
        info = cursor.fetchall()
        if not info:
            print("joined")
            cursor.execute("INSERT INTO joined_events (name_events, user_id) VALUES (?,?)", (events[0][0],id[0]))
            conn.commit()
            conn.close()

    return render_template('eventpage.html',name_author=username_author[0], name_event=event_name, info_event=events[0][1], start_date=events[0][2], end_date=events[0][3])
'''

'''
@app.route('/about-me/<name>/<age>')
def about(name, age):
    return name + " " + age + " y. o."'''
'''
app.run(debug=True)
'''