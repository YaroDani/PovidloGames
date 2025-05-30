from utils.util import get_db_connection

def get_info_a_event(event_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_events, info, start_date, end_date, user_id FROM events WHERE name_events = ?", (event_name,))
    data = cursor.fetchall()
    conn.close()
    return data


def create_game(name_event, info, start_date, end_date, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (name_events, info, start_date, end_date, user_id) VALUES (?, ?, ?, ?, ?)",
                   (name_event, info, start_date, end_date, user_id))
    conn.commit()
    conn.close()


def get_all_events():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_events, start_date FROM events ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data


def get_user_name(name):
    return name.strip()
