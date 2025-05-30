import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    info TEXT,
    pfp BLOB
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
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS joined_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_events TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    author_id INTEGER
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    file_data BLOB,
    file_name TEXT,
    user_id INTEGER,
    created_at TEXT,
    event_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS game_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    image_data BLOB,
    image_name TEXT,
    FOREIGN KEY (game_id) REFERENCES games(id)
)
''')
conn.commit()
conn.close()
