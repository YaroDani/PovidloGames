import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_events TEXT NOT NULL,
    info TEXT,
    start_date TEXT,
    end_date TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
)
''')

conn.commit()
conn.close()
