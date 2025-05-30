import sqlite3
from datetime import datetime

def get_db_connection():
    return sqlite3.connect('users.db')


def validate_name(name_event):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE name_events = ?", (name_event,))
    exists = cursor.fetchone()
    conn.close()
    return not exists  # True якщо не існує


def validate_date(start_date, end_date):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    except:
        return False
