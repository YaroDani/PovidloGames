from flask import render_template, session, Blueprint, request, redirect, url_for
from models.users import check_email_name, check_email_password, save_data

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if request.method == "POST":
        if email and password and username:
            error = check_email_name(email,username)
            if not error:
                save_data(email,username,password)
                return redirect(url_for('home.home'))

    session['username'] = username
    session['email'] = email
    return render_template('register.html', error=error)

@bp.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user=check_email_password(email,password)
            if user:
                if user[3] == password:
                    session['username'] = user[2]
                    session['email'] = user[1]
                    return redirect(url_for('home.home'))
                else:
                    error = 'Password error'
            else:
                error = 'Email error'

    return render_template('login.html', error=error)

@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
