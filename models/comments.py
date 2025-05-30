from utils.util import get_db_connection

'''cursor.execute(
        "INSERT INTO events (name_events, info, start_date, end_date, user_id) VALUES (?, ?, ?, ?, ?)",
        (name_event, info, start_date, end_date, user_id))'''

def add_comment(user_id,text,author_id):
    conn=get_db_connection()
    cursor=conn.cursor()
    cursor.execute('INSERT INTO comments (user_id, text, author_id) VALUES (?,?,?)', (user_id,text,author_id))


def get_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, text, author_id FROM comments")
    comments = cursor.fetchone()
    conn.close()
    return comments
