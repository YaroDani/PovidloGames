from flask import Flask
from routes.register import bp as auth_bp
from routes.home import bp as home_bp
from routes.main import bp as main_bp
from routes.profiles import bp as profiles_bp
from routes.games import bp as games_bp

app = Flask(__name__)
app.secret_key = '123'

# Реєстрація всіх Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(main_bp)
app.register_blueprint(profiles_bp)
app.register_blueprint(games_bp)

if __name__ == '__main__':
    app.run(debug=True)
