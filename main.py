from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn
    # cursor = conn.cursor()


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'


@app.route('/')  # головна сторінка logika.com
def main_page():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])  # сторінка logika.com/register
def register():
    error = None
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if request.method == "POST":
        if email and password and username:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))  # отримати всі елементи з email
            user = cursor.fetchone()
            if user:
                error = 'Такий користувач вже існує'
                conn.close()
            else:
                cursor.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                               (email, username, password))
                conn.commit()
                conn.close()

                session['username'] = username
                session['email'] = email
                return redirect(url_for('home'))

    return render_template('register.html', error=error)


@app.route('/login', methods=['POST', 'GET'])  # сторінка logika.com/login
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=?", (email,))  # отримати всі елементи з email
            user = cursor.fetchone()
            conn.close()

            if user:
                if user[3] == password:

                    session['username'] = user[2]
                    session['email'] = user[1]
                    return redirect(url_for('home'))
                else:
                    error = 'Пароль'
            else:
                error = 'Пошта'

    return render_template('login.html', error=error)


@app.route('/home', methods=['POST', 'GET'])
def home():
    return render_template('home.html', username=session['username'], email=session['email'])


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))


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


@app.route('/games-events', methods=['POST', 'GET'])
def games():
    start = None
    error = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'start':
            start = True
        if action == 'create':
            name_event = request.form.get('name_event')
            info = request.form.get('info')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
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

                if name_event and start_date and end_date:
                    cursor.execute(
                        "INSERT INTO events (name_events, info, start_date, end_date, user_id) VALUES (?, ?, ?, ?, ?)",
                        (name_event, info, start_date, end_date, user_id))
                    conn.commit()
                    conn.close()
                else:
                    error = 'Будь ласка перевірте чи всі поля заповнені'
            else:
                error = 'Дата неправильна'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_events, start_date FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template('games_events.html', start=start, error=error, events=events)


'''
@app.route('/about-me/<name>/<age>')
def about(name, age):
    return name + " " + age + " y. o."'''

app.run(debug=True)
