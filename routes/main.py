from flask import render_template, session, Blueprint
from models.users import get_user_role

bp = Blueprint('main', __name__)


@bp.route('/')  # головна сторінка logika.com
def main_page():
    show_button=None

    if len(session)>0:
        role=get_user_role(session['email'])
        try:
            if role[0] == "admin":
                show_button=True
            else:
                show_button=False
        except Exception as e:
            print(e)
    return render_template('main.html', show_button=show_button)
