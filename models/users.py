from utils.util import get_db_connection


def get_user_id(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email=?', (email,))
    user = cursor.fetchone()
    return user


def get_user_role(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE email=?", (email,))
    role=cursor.fetchone()
    return role


def check_email_name (email,username):
    error = None
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email=?", (email,))
    user_email = cursor.fetchone()
    cursor.execute("SELECT username FROM users WHERE username=?", (username,))
    user_name = cursor.fetchone()
    if user_email:
        error = 'Email already exists'
        conn.close()
    elif user_name:
        error = "username already exists"
        conn.close()
    return error


def check_email_password(email,password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user


def save_data(email,username,password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, username, password, role) VALUES (?, ?, ?, ?)",
                   (email, username, password, "user"))
    conn.commit()
    conn.close()


def get_all_info(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
    user_id = cursor.fetchone()
    cursor.execute("SELECT role FROM users WHERE email=?", (email,))
    role = cursor.fetchone()
    cursor.execute("SELECT name_events, start_date FROM events WHERE user_id=?", (user_id[0],))
    events = cursor.fetchall()
    cursor.execute("SELECT name_events FROM joined_events WHERE user_id=? ", (user_id[0],))
    joined_events = cursor.fetchall()
    conn.close()
    return user_id, role, events, joined_events


def start_game(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id,role FROM users WHERE email = ?', (email,))
    user_info = cursor.fetchone()
    cursor.execute("SELECT name_events FROM events WHERE user_id=?", (user_info[0],))
    events = cursor.fetchall()
    events_count = len(events)
    return user_info, events_count

def update_info(user_id, name, info, pfp):
    conn = get_db_connection()
    cursor = conn.cursor()
    #cursor.execute('DELETE FROM users WHERE user_id-?', (user_id, )) видалення з бд
    #cursor.execute('REPLACE INTO user (username, info, pfp) VALUES (?, ?, ?)', ()) пперезапис

