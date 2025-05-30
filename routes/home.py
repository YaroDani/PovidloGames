from flask import render_template, session, Blueprint, request, redirect, url_for, send_file, flash
from utils.util import get_db_connection
from models.users import get_all_info, get_user_id
import io
import re
from mimetypes import guess_type
from datetime import datetime

bp = Blueprint('home', __name__)

def clean_filename(filename):
    return re.sub(r'[^A-Za-z0-9_.-]', '_', filename)

@bp.route('/home', methods=['POST', 'GET'])
def home():
    print('[HOME] --- СТАРТ ---', request.method)
    if 'email' not in session or not session['email']:
        print('[HOME] Немає email у сесії або сесія пуста')
        return redirect(url_for('auth.login'))

    comments = None
    joined_events = []
    events = []
    role = None
    start = False

    if request.method == 'POST':
        print('[POST] --- ПОЧАТОК ОБРОБКИ ---')
        try:
            action = request.form.get('start') or request.form.get('save')
            print('[POST] action:', action)
            print('[POST] form:', request.form)
            print('[POST] files:', request.files)
            if action == 'start':
                print('[POST] Обрано "start"')
                start = True
            elif action == 'save':
                print('[POST] Обрано "save"')
                # --- Витягуємо user_id
                user_id_row = get_user_id(session['email'])
                print('[POST] user_id_row:', user_id_row)
                if not user_id_row:
                    print('[POST] user_id_row is None! Перенаправляємо на логін')
                    return redirect(url_for('auth.login'))
                user_id = user_id_row[0]
                print('[POST] user_id:', user_id)
                conn = get_db_connection()
                row = conn.execute("SELECT username, pfp FROM users WHERE id = ?", (user_id,)).fetchone()
                print('[POST] Поточні дані користувача:', row)
                old_name = row[0] if row else None
                old_pfp = row[1] if row else None

                name = request.form.get('username')
                print('[POST] Ім\'я з форми:', name)
                file = request.files.get('file')
                print('[POST] Файл з форми:', file, file.filename if file else None)

                if not name:
                    print('[POST] Не введено нове ім\'я, залишаємо старе')
                    name = old_name
                if file and file.filename:
                    data = file.read()
                    print('[POST] Файл є, розмір:', len(data))
                    conn.execute("UPDATE users SET username = ?, pfp = ? WHERE id = ?", (name, data, user_id))
                else:
                    print('[POST] Файлу нема, оновлюємо тільки ім\'я')
                    conn.execute("UPDATE users SET username = ? WHERE id = ?", (name, user_id))
                conn.commit()
                print('[POST] Зберігаємо дані у БД...')
                row2 = conn.execute("SELECT username, pfp FROM users WHERE id = ?", (user_id,)).fetchone()
                print('[POST] Дані після оновлення:', row2)
                conn.close()
                session['username'] = name
                start = False
            else:
                print('[POST] Незнайома дія:', action)
        except Exception as e:
            print('[POST][ERROR]:', e)

    try:
        print('[GET ALL INFO] Витягуємо дані для сторінки профілю...')
        user_id, role, events, joined_events = get_all_info(session['email'])
        print('[GET ALL INFO] OK:', user_id, role, events, joined_events)
    except Exception as e:
        print('[GET ALL INFO][ERROR]:', e)
        user_id = None
        role = None
        events = []
        joined_events = []

    if joined_events:
        joined_events = [row[0] for row in joined_events]
        print('[INFO] joined_events:', joined_events)
    else:
        print('[INFO] joined_events порожній')
    print('[RENDER] Передаємо дані у шаблон...')
    return render_template(
        'home.html',
        username=session.get('username'),
        email=session.get('email'),
        events=events,
        joined_events=joined_events,
        role=role,
        comments=comments,
        start=start,
        current_time=datetime.now().timestamp()
    )

@bp.route('/pfp/email/<email>')
def pfp_by_email(email):
    print('[AVATAR] Запит на аватар для:', email)
    conn = get_db_connection()
    row = conn.execute("SELECT pfp FROM users WHERE email = ?", (email,)).fetchone()
    print('[AVATAR] Результат SQL:', row)
    conn.close()
    if row and row[0]:
        mime_type = guess_type("file.png")[0] or 'image/png'
        print('[AVATAR] Віддаємо файл-аватар')
        return send_file(io.BytesIO(row[0]), mimetype=mime_type)
    print('[AVATAR] Аватар не знайдено, редірект на placeholder')
    return redirect("https://via.placeholder.com/150")


@bp.route('/add-game', methods=['GET', 'POST'])
def add_game():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    user_id = get_user_id(session['email'])[0]

    # Отримати id івента із GET чи POST (form)
    event_id = request.args.get('event_id') or request.form.get('event_id')
    event_name = None

    # Якщо передано event_id, дістаємо назву івента для підпису в шаблоні
    if event_id:
        conn = get_db_connection()
        row = conn.execute('SELECT name_events FROM events WHERE id=?', (event_id,)).fetchone()
        if row:
            event_name = row[0]
        conn.close()

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('file')
        images = request.files.getlist('images')
        created_at = datetime.now().isoformat()

        if not title or not file:
            flash('Назва гри та файл обовʼязкові!')
            return redirect(request.url)

        file_data = file.read()
        file_name = file.filename

        conn = get_db_connection()
        cursor = conn.cursor()

        # Додаємо гру (з event_id якщо є)
        cursor.execute('''
            INSERT INTO games (title, description, file_data, file_name, user_id, event_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, file_data, file_name, user_id, event_id, created_at))
        game_id = cursor.lastrowid

        # Додаємо всі картинки (gallery)
        for img in images:
            if img and img.filename:
                img_data = img.read()
                cursor.execute('''INSERT INTO game_images (game_id, image_data, image_name) VALUES (?, ?, ?)''',
                               (game_id, img_data, img.filename))
        conn.commit()
        conn.close()
        flash('Гру успішно додано!')
        return redirect(url_for('games.games_gallery'))

    return render_template('add_game.html', event_id=event_id, event_name=event_name)

