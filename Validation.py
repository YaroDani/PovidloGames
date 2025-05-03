import sqlite3


def validate_date(start_date, end_date):
    data_s = list(map(int, start_date.split("-")))
    date_e = list(map(int, end_date.split("-")))
    if data_s[0] == date_e[0]:
        data_s[1] -= 1
        date_e[1] -= 1
        data_s[1] *= 30
        date_e[1] *= 30

        if data_s[0] + data_s[1] + data_s[2] < date_e[0] + date_e[1] + date_e[2]:
            #print("Все правильно")
            return True
        else:
            #print("Дата кінця раніша за початок")
            return False

    elif data_s[0] < date_e[0]:
        #print("Все правильно")
        return True
    else:
        #print("Дата кінця раніша за початок")
        return False

'''    
start_date = input('Y-m-d: ')
end_date= input('Y-M-D:')
start_date='2025-04-05'
end_date='2025-04-06'
print(validate_date(start_date,end_date))'''

def get_db_connection():
    conn = sqlite3.connect("users.db")
    return conn
    # cursor = conn.cursor()


def validate_name(name_event):
    cursor = get_db_connection()
    cursor.execute('SELECT id FROM events WHERE name_events = ?', (name_event, ))
    result = cursor.fetchone()
    if result:
        print('Назва вже зайнята')


def event_page(event_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name_events, info, start_date, end_date, user_id FROM events WHERE name_events = ?",
                   (event_name,))
    events = cursor.fetchall()  # id_user [0][4]

    username = cursor.execute("SELECT username FROM users WHERE id = ?", (events[0][4], ))
    username = username.fetchone()
    print(username)

event_page("First")